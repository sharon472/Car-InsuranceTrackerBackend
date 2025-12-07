# migrations/versions/9f62baa1dbc3_initial_tables.py

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '9f62baa1dbc3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. EMPLOYEES (ORIGINAL)
    op.create_table('employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 2. USERS (DBML)
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    
    # 3. CARS (HYBRID)
    op.create_table('cars',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plate_number', sa.String(length=20), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        
        # ORIGINAL FIELDS
        sa.Column('assigned_id', sa.Integer(), nullable=True),
        sa.Column('insurance_due', sa.Date(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        
        # DBML FIELDS
        sa.Column('owner_name', sa.String(length=100), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True), 
        
        # FOREIGN KEYS
        sa.ForeignKeyConstraint(['assigned_id'], ['employees.id'], ), # ORIGINAL
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),         # DBML
        
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cars_id'), 'cars', ['id'], unique=False)
    op.create_index(op.f('ix_cars_plate_number'), 'cars', ['plate_number'], unique=True)
    
    # 4. INSURANCES (HYBRID)
    op.create_table('insurances',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('car_id', sa.Integer(), nullable=True),
        
        # ORIGINAL FIELDS
        sa.Column('company', sa.String(length=100), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('premium', sa.Integer(), nullable=True),
        
        # DBML FIELD
        sa.Column('status', sa.String(length=20), nullable=True),
        
        sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('insurances')
    op.drop_table('cars')
    op.drop_table('users')
    op.drop_table('employees')
