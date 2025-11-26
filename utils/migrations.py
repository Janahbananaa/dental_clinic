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
            
            print("Running database migrations...")
            
            # Add is_deleted column to patients table
            self._add_is_deleted_to_patients(cursor, conn)
            
            # Add is_deleted column to doctors table
            self._add_is_deleted_to_doctors(cursor, conn)
            
            # Add is_deleted column to appointments table
            self._add_is_deleted_to_appointments(cursor, conn)
            
            # Add is_deleted column to billing table
            self._add_is_deleted_to_billing(cursor, conn)
            
            cursor.close()
            conn.close()
            print("✓ All migrations completed successfully")
            return True
            
        except mysql.connector.Error as err:
            print(f"✗ Migration error: {err}")
            return False
    
    def _add_is_deleted_to_patients(self, cursor, conn):
        """Add is_deleted column to patients table"""
        try:
            cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='patients' AND COLUMN_NAME='is_deleted'")
            if cursor.fetchone():
                print("  • is_deleted column already exists in patients table")
                return
            
            cursor.execute("""
                ALTER TABLE patients 
                ADD COLUMN is_deleted TINYINT(1) DEFAULT 0
            """)
            conn.commit()
            print("  ✓ Added is_deleted column to patients table")
        except mysql.connector.Error as err:
            print(f"  ✗ Error adding is_deleted to patients: {err}")
            conn.rollback()
    
    def _add_is_deleted_to_doctors(self, cursor, conn):
        """Add is_deleted column to doctors table"""
        try:
            cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='doctors' AND COLUMN_NAME='is_deleted'")
            if cursor.fetchone():
                print("  • is_deleted column already exists in doctors table")
                return
            
            cursor.execute("""
                ALTER TABLE doctors 
                ADD COLUMN is_deleted TINYINT(1) DEFAULT 0
            """)
            conn.commit()
            print("  ✓ Added is_deleted column to doctors table")
        except mysql.connector.Error as err:
            print(f"  ✗ Error adding is_deleted to doctors: {err}")
            conn.rollback()
    
    def _add_is_deleted_to_appointments(self, cursor, conn):
        """Add is_deleted column to appointments table"""
        try:
            cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='appointments' AND COLUMN_NAME='is_deleted'")
            if cursor.fetchone():
                print("  • is_deleted column already exists in appointments table")
                return
            
            cursor.execute("""
                ALTER TABLE appointments 
                ADD COLUMN is_deleted TINYINT(1) DEFAULT 0
            """)
            conn.commit()
            print("  ✓ Added is_deleted column to appointments table")
        except mysql.connector.Error as err:
            print(f"  ✗ Error adding is_deleted to appointments: {err}")
            conn.rollback()
    
    def _add_is_deleted_to_billing(self, cursor, conn):
        """Add is_deleted column to billing table"""
        try:
            cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='billing' AND COLUMN_NAME='is_deleted'")
            if cursor.fetchone():
                print("  • is_deleted column already exists in billing table")
                return
            
            cursor.execute("""
                ALTER TABLE billing 
                ADD COLUMN is_deleted TINYINT(1) DEFAULT 0
            """)
            conn.commit()
            print("  ✓ Added is_deleted column to billing table")
        except mysql.connector.Error as err:
            print(f"  ✗ Error adding is_deleted to billing: {err}")
            conn.rollback()
