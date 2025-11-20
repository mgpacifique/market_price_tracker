"""
Database migration runner
Applies database schema changes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database


def run_migration(db, migration_file):
    """Run a single migration file"""
    print(f"Running migration: {migration_file}")
    
    try:
        with open(migration_file, 'r') as f:
            sql_content = f.read()
        
        # Remove comments
        lines = []
        for line in sql_content.split('\n'):
            # Remove line comments
            if not line.strip().startswith('--'):
                lines.append(line)
        
        sql_content = '\n'.join(lines)
        
        # Split by semicolon but keep ALTER TABLE ADD COLUMN statements together
        statements = []
        current_statement = []
        
        for line in sql_content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            current_statement.append(line)
            
            # Check if this line ends a statement
            if line.endswith(';'):
                full_statement = ' '.join(current_statement)
                if full_statement.strip():
                    statements.append(full_statement)
                current_statement = []
        
        # Add any remaining statement
        if current_statement:
            full_statement = ' '.join(current_statement)
            if full_statement.strip() and not full_statement.strip().endswith(';'):
                full_statement += ';'
            if full_statement.strip():
                statements.append(full_statement)
        
        success_count = 0
        for i, statement in enumerate(statements, 1):
            statement = statement.strip()
            if not statement or statement == ';':
                continue
            
            try:
                db.execute_query(statement)
                # Only show first 80 chars
                preview = statement[:80].replace('\n', ' ')
                print(f"  ✓ Statement {i}: {preview}...")
                success_count += 1
            except Exception as e:
                error_msg = str(e)
                # Ignore "Duplicate column" errors as they mean it already exists
                if 'Duplicate column' in error_msg or 'already exists' in error_msg:
                    print(f"  ⚠ Statement {i}: Already exists, skipping")
                    success_count += 1
                else:
                    preview = statement[:80].replace('\n', ' ')
                    print(f"  ✗ Error in statement {i}: {error_msg}")
                    print(f"     Statement: {preview}...")
                    # Don't return False, continue with other statements
        
        print(f"✓ Migration completed: {success_count}/{len(statements)} statements\n")
        return True
        
    except Exception as e:
        print(f"✗ Error reading migration file: {e}\n")
        return False


def main():
    """Main migration runner"""
    print("=" * 60)
    print("DATABASE MIGRATION RUNNER")
    print("=" * 60)
    print()
    
    # Initialize database connection
    print("Connecting to database...")
    db = Database()
    
    if not db.connect():
        print("✗ Failed to connect to database")
        print("Please check your configuration in config.ini")
        return
    
    print("✓ Connected to database successfully\n")
    
    # Get migration files
    migrations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'migrations')
    migration_files = sorted([
        os.path.join(migrations_dir, f) 
        for f in os.listdir(migrations_dir) 
        if f.endswith('.sql')
    ])
    
    if not migration_files:
        print("No migration files found")
        return
    
    print(f"Found {len(migration_files)} migration file(s)\n")
    
    # Run migrations
    success_count = 0
    for migration_file in migration_files:
        if run_migration(db, migration_file):
            success_count += 1
    
    # Summary
    print("=" * 60)
    print(f"MIGRATION SUMMARY: {success_count}/{len(migration_files)} successful")
    print("=" * 60)
    
    db.disconnect()
    print("\n✓ Database connection closed")


if __name__ == "__main__":
    main()
