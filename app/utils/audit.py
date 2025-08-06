from app.models.audit_log import AuditLog

def log_action(db, user_id, action):
    log = AuditLog(user_id=user_id, action=action)
    db.add(log)
    db.commit()
