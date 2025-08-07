from app.models.audit_log import AuditLog

def log_action(db, user_email, action):
    log = AuditLog(user_email=user_email, action=action)
    db.add(log)
    db.commit()
