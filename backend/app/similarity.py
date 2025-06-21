import asyncpg
from typing import List, Dict, Any
import numpy as np

async def get_top_similar_projects(
    embedding: List[float],
    top_n: int = 5,
    db_url: str = None
) -> List[Dict[str, Any]]:
    """
    Given an input embedding, return top N similar projects from the database using pgvector cosine similarity.
    Args:
        embedding: List of floats representing the input embedding.
        top_n: Number of top similar projects to return.
        db_url: Database connection string.
    Returns:
        List of dicts with project info and similarity score.
    """
    if db_url is None:
        raise ValueError("Database URL must be provided.")

    conn = await asyncpg.connect(dsn=db_url)
    try:
        # Convert embedding to Postgres array string
        embedding_str = str(embedding).replace('[', '{').replace(']', '}')
        query = f'''
            SELECT id, title, description, embedding,
                   1 - (embedding <=> $1::vector) AS similarity
            FROM projects
            ORDER BY embedding <=> $1::vector
            LIMIT {top_n}
        '''
        rows = await conn.fetch(query, embedding)
        results = []
        for row in rows:
            results.append({
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'similarity': float(row['similarity'])
            })
        return results
    finally:
        await conn.close()
