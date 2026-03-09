from functools import wraps
from flask import session, redirect


# ===============================
# LOGIN OBRIGATÓRIO
# ===============================

def login_obrigatorio(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "usuario_id" not in session and "aluno_id" not in session:
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated_function


# ===============================
# SOMENTE ADMIN
# ===============================

def admin_obrigatorio(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "perfil" not in session:
            return redirect("/login")

        if session["perfil"] != "admin":
            return "Acesso negado"

        return f(*args, **kwargs)

    return decorated_function


# ===============================
# STAFF (ADMIN / SUPORTE)
# ===============================

def staff_obrigatorio(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "perfil" not in session:
            return redirect("/login")

        if session["perfil"] not in ["admin","suporte"]:
            return "Acesso negado"

        return f(*args, **kwargs)

    return decorated_function