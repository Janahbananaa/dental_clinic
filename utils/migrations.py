import mysql.connector
from config import DB_CONFIG


class DatabaseMigrations:
    """Handle database schema migrations"""
    
    def __init__(self):
        self.config = DB_CONFIG
    
    def run_migrations(self):
        """Run all pending migrations"""
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            
            # Migration 1: Add Address column to appointments table
            try:
                cursor.execute("""
                    ALTER TABLE appointments 
                    ADD COLUMN Address VARCHAR(200) NULL DEFAULT NULL
                """)
                conn.commit()
                print("✓ Migration: Added Address column to appointments table")
            except mysql.connector.Error as e:
                if "Duplicate column name" in str(e):
                    print("✓ Migration: Address column already exists in appointments table")
                else:
                    print(f"✗ Migration error: {e}")
                    return False
            
            # Migration 2: Add Address column to billing table
            try:
                cursor.execute("""
                    ALTER TABLE billing 
                    ADD COLUMN Address VARCHAR(200) NULL DEFAULT NULL
                """)
                conn.commit()
                print("✓ Migration: Added Address column to billing table")
            except mysql.connector.Error as e:
                if "Duplicate column name" in str(e):
                    print("✓ Migration: Address column already exists in billing table")
                else:
                    print(f"✗ Migration error: {e}")
                    return False
            
            cursor.close()
            conn.close()
            print("✓ All migrations completed successfully")
            return True
            
        except mysql.connector.Error as err:
            print(f"✗ Migration failed: {err}")
            return False
    
    def _column_exists(self, cursor, db_name, table_name, column_name):
        """Check if a column exists in a table"""
        try:
            query = f"""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
                       WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s"""
            cursor.execute(query, (db_name, table_name, column_name))
            return cursor.fetchone() is not None
        except mysql.connector.Error:
            return False
    
    def _add_is_deleted_to_table(self, cursor, conn, db_name, table_name):
        """Add is_deleted column to a table if it doesn't exist"""
        try:
            if self._column_exists(cursor, db_name, table_name, 'is_deleted'):
                print(f"  • is_deleted column already exists in {table_name} table")
                return
            
            cursor.execute(f"""
                ALTER TABLE {table_name} 
                ADD COLUMN is_deleted TINYINT(1) DEFAULT 0
            """)
            conn.commit()
            print(f"  ✓ Added is_deleted column to {table_name} table")
        except mysql.connector.Error as err:
            print(f"  ✗ Error adding is_deleted to {table_name}: {err}")
            conn.rollback()
    
    def _create_dentist_schedule_table(self, cursor, conn):
        """Create dentist_schedule table if it doesn't exist"""
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dentist_schedule (
                    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
                    dentist_id INT NOT NULL,
                    `date` DATE NOT NULL,
                    `start_time` TIME NOT NULL,
                    `end_time` TIME NOT NULL,
                    location VARCHAR(100),
                    status ENUM('Available', 'Busy', 'Off') DEFAULT 'Available',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (dentist_id) REFERENCES doctors(dentist_id) ON DELETE CASCADE
                )
            """)
            conn.commit()
            print("  ✓ dentist_schedule table created/verified")
        except mysql.connector.Error as err:
            if "already exists" in str(err):
                print("  • dentist_schedule table already exists")
            else:
                print(f"  ✗ Error creating dentist_schedule table: {err}")
            conn.rollback()
