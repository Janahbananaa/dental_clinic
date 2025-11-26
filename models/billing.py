from typing import Optional

class Billing:
    def __init__(self, db, billing_id: int = None, appointment_id: int = None,
                 name: str = "", dental_service: str = "", service_fee: float = 0.0,
                 total_fee: float = 0.0, date_time: str = "", payment_method: str = "Cash", 
                 status: str = "Pending"):
        self.db = db
        self.billing_id = billing_id
        self.appointment_id = appointment_id
        self.name = name
        self.dental_service = dental_service
        self.service_fee = service_fee
        self.total_fee = total_fee
        self.date_time = date_time
        self.payment_method = payment_method
        self.status = status
    
    def save(self) -> bool:
        if self.billing_id:
            query = """UPDATE billing SET appointment_id=%s, Name=%s, Dental_service=%s, 
                      Service_fee=%s, Total_fee=%s, `Date/Time`=%s, Payment_method=%s, Status=%s 
                      WHERE billing_id=%s"""
            return self.db.execute_query(query, (self.appointment_id, self.name,
                                                  self.dental_service, self.service_fee,
                                                  self.total_fee, self.date_time,
                                                  self.payment_method, self.status, self.billing_id))
        else:
            query = """INSERT INTO billing (appointment_id, Name, Dental_service, Service_fee, 
                      Total_fee, `Date/Time`, Payment_method, Status) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            return self.db.execute_query(query, (self.appointment_id, self.name,
                                                  self.dental_service, self.service_fee,
                                                  self.total_fee, self.date_time,
                                                  self.payment_method, self.status))
    
    @staticmethod
    def get_all(db) -> list:
        query = "SELECT * FROM billing ORDER BY billing_id DESC"
        return db.fetch_all(query)
    
    @staticmethod
    def get_by_appointment(db, appointment_id: int) -> Optional['Billing']:
        query = "SELECT * FROM billing WHERE appointment_id=%s"
        result = db.fetch_one(query, (appointment_id,))
        if result:
            return Billing(db, result['billing_id'], result['appointment_id'],
                         result.get('Name', ''), result.get('Dental_service', ''),
                         result.get('Service_fee', 0.0), result.get('Total_fee', 0.0),
                         result.get('Date/Time', ''), result.get('Payment_method', 'Cash'), 
                         result.get('Status', 'Pending'))
        return None
    
    def mark_completed(self) -> bool:
        if self.billing_id:
            self.status = "Completed"
            query = "UPDATE billing SET Status=%s WHERE billing_id=%s"
            return self.db.execute_query(query, (self.status, self.billing_id))
        return False
    
    def delete(self) -> bool:
        if self.billing_id:
            query = "DELETE FROM billing WHERE billing_id=%s"
            return self.db.execute_query(query, (self.billing_id,))
        return False
