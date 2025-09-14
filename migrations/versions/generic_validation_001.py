"""Generic validation schema migration

Revision ID: generic_validation_001
Revises: 6cde8b243f7d
Create Date: 2025-09-13 22:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'generic_validation_001'
down_revision = '6cde8b243f7d'
branch_labels = None
depends_on = None

def upgrade():
    # Add new generic columns
    op.add_column('validation_history', sa.Column('validation_data', sa.Text(), nullable=True))
    op.add_column('validation_history', sa.Column('validation_rules', sa.Text(), nullable=True))
    
    # Create document_embeddings table
    op.create_table('document_embeddings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('document_id', sa.String(), nullable=True),
        sa.Column('source_file', sa.String(), nullable=True),
        sa.Column('chunk_text', sa.Text(), nullable=True),
        sa.Column('chunk_index', sa.Integer(), nullable=True),
        sa.Column('embedding_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_document_embeddings_document_id'), 'document_embeddings', ['document_id'], unique=True)
    
    # Migrate existing data from ein/duns to generic format
    connection = op.get_bind()
    result = connection.execute('SELECT id, ein, duns FROM validation_history')
    for row in result:
        if row.ein or row.duns:
            data = {}
            rules = {}
            if row.ein:
                data['ein'] = row.ein
                rules['ein'] = 'pattern:^\\d{9}$'
            if row.duns:
                data['duns'] = row.duns
                rules['duns'] = 'pattern:^\\d{9}$'
            
            connection.execute(
                f"UPDATE validation_history SET validation_data = '{str(data)}', validation_rules = '{str(rules)}' WHERE id = {row.id}"
            )
    
    # Drop old columns
    op.drop_column('validation_history', 'ein')
    op.drop_column('validation_history', 'duns')

def downgrade():
    # Add back old columns
    op.add_column('validation_history', sa.Column('ein', sa.String(), nullable=True))
    op.add_column('validation_history', sa.Column('duns', sa.String(), nullable=True))
    
    # Drop new columns
    op.drop_column('validation_history', 'validation_data')
    op.drop_column('validation_history', 'validation_rules')
    
    # Drop document_embeddings table
    op.drop_index(op.f('ix_document_embeddings_document_id'), table_name='document_embeddings')
    op.drop_table('document_embeddings')
