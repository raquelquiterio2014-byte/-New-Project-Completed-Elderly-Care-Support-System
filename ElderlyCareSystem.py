import customtkinter as ctk
import sqlite3
from datetime import datetime
import os
import sys


# ==========================
# VISUAL SETTINGS
# ==========================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

AZUL_ESCURO = "#003366"
AZUL_MEDIO = "#004C99"
AZUL_SIDEBAR = "#062B55"
AZUL_BOTAO = "#073B75"
AZUL_HOVER = "#0B5CAD"

# Soft lilac background
FUNDO = "#F8F3FF"
FUNDO_CARD = "#FFFFFF"
BORDA_CARD = "#E2D9F3"


# ==========================
# DATABASE PATH
# ==========================

def caminho_banco():

    if getattr(sys, "frozen", False):
        pasta_base = os.path.dirname(sys.executable)
    else:
        pasta_base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(pasta_base, "cuidados_idoso.db")


def conectar():
    return sqlite3.connect(caminho_banco())


def coluna_existe(cursor, tabela, coluna):
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [c[1] for c in cursor.fetchall()]
    return coluna in colunas


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        idade TEXT,
        telefone TEXT,
        tipo TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        tipo TEXT,
        dose TEXT,
        horario TEXT,
        observacao TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS atividades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT,
        horario TEXT,
        status TEXT,
        observacao TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ocorrencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT,
        gravidade TEXT,
        data TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        remetente TEXT,
        mensagem TEXT,
        data TEXT
    )
    """)

    # Automatic update for older databases
    if not coluna_existe(cursor, "ocorrencias", "solucao"):
        cursor.execute("ALTER TABLE ocorrencias ADD COLUMN solucao TEXT")

    if not coluna_existe(cursor, "ocorrencias", "responsavel"):
        cursor.execute("ALTER TABLE ocorrencias ADD COLUMN responsavel TEXT")

    conn.commit()
    conn.close()


# ==========================
# APPLICATION
# ==========================

class SistemaCuidados(ctk.CTk):

    def __init__(self):
        super().__init__()

        criar_tabelas()

        self.title("Elderly Care Support System")
        self.geometry("1050x650")
        self.minsize(900, 600)
        self.resizable(True, True)
        self.configure(fg_color=FUNDO)

        self.sidebar = ctk.CTkFrame(
            self,
            width=235,
            fg_color=AZUL_SIDEBAR,
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.conteudo = ctk.CTkFrame(
            self,
            fg_color=FUNDO,
            corner_radius=0
        )
        self.conteudo.pack(side="right", fill="both", expand=True)

        self.criar_menu()
        self.tela_dashboard()

    # ==========================
    # GENERAL FUNCTIONS
    # ==========================

    def limpar_tela(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def criar_menu(self):
        ctk.CTkLabel(
            self.sidebar,
            text="💙 Elderly Care\n Support System",
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        ).pack(pady=20)

        botoes = [
            ("🏠  Dashboard", self.tela_dashboard),
            ("👤  1  Users", self.tela_usuarios),
            ("💊  2  Medications", self.tela_medicamentos),
            ("📅  3  Routine", self.tela_rotina),
            ("⚠️  4  Occurrences", self.tela_ocorrencias),
            ("🔔  5  Alerts", self.tela_alertas),
            ("📄  6  Daily Report", self.tela_relatorio_diario),
            ("🧑‍⚕️  7  Caregiver Panel", self.tela_painel_cuidador),
            ("👴  8  Elderly Panel", self.tela_painel_idoso),
            ("💬  9  Communication", self.tela_comunicacao),
            ("📊  10 Final Report", self.tela_relatorio_final),
        ]

        for texto, comando in botoes:
            ctk.CTkButton(
                self.sidebar,
                text=texto,
                command=comando,
                width=205,
                height=35,
                anchor="w",
                font=("Segoe UI", 13),
                fg_color=AZUL_BOTAO,
                hover_color=AZUL_HOVER,
                text_color="white",
                corner_radius=8
            ).pack(pady=3)

        ctk.CTkButton(
            self.sidebar,
            text="🚪  0  Exit",
            command=self.destroy,
            width=205,
            height=35,
            anchor="w",
            font=("Segoe UI", 13),
            fg_color="#0B1F3A",
            hover_color="#B22222",
            text_color="white",
            corner_radius=8
        ).pack(pady=15)

    def criar_titulo(self, texto, subtitulo=""):
        ctk.CTkLabel(
            self.conteudo,
            text=texto,
            font=("Segoe UI", 26, "bold"),
            text_color=AZUL_ESCURO
        ).pack(pady=(18, 4))

        if subtitulo:
            ctk.CTkLabel(
                self.conteudo,
                text=subtitulo,
                font=("Segoe UI", 13),
                text_color=AZUL_MEDIO
            ).pack(pady=(0, 10))

    def contar_registros(self, tabela):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
        total = cursor.fetchone()[0]
        conn.close()
        return total

    def criar_card_dashboard(self, parent, icone, titulo, texto, row, col):
        card = ctk.CTkFrame(
            parent,
            width=260,
            height=110,
            fg_color=FUNDO_CARD,
            border_color=BORDA_CARD,
            border_width=1,
            corner_radius=15
        )
        card.grid(row=row, column=col, padx=15, pady=12)
        card.grid_propagate(False)

        ctk.CTkLabel(card, text=icone, font=("Segoe UI Emoji", 34)).place(x=22, y=34)

        ctk.CTkLabel(
            card,
            text=titulo,
            font=("Segoe UI", 16, "bold"),
            text_color=AZUL_ESCURO
        ).place(x=85, y=25)

        ctk.CTkLabel(
            card,
            text=texto,
            font=("Segoe UI", 12),
            text_color=AZUL_MEDIO,
            justify="left"
        ).place(x=85, y=55)

    def deletar_por_id(self, tabela, id_registro, callback):
        if not id_registro.strip():
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {tabela} WHERE id=?", (id_registro,))
        conn.commit()
        conn.close()

        callback()

    # ==========================
    # DASHBOARD
    # ==========================

    def tela_dashboard(self):
        self.limpar_tela()

        self.criar_titulo(
            "General Dashboard",
            "Quick monitoring of patient care, alerts, and reports."
        )

        area_cards = ctk.CTkFrame(self.conteudo, fg_color=FUNDO)
        area_cards.pack(pady=5)

        usuarios = self.contar_registros("usuarios")
        medicamentos = self.contar_registros("medicamentos")
        atividades = self.contar_registros("atividades")
        ocorrencias = self.contar_registros("ocorrencias")
        mensagens = self.contar_registros("mensagens")

        self.criar_card_dashboard(area_cards, "👤", "Users", f"{usuarios} registered\nuser(s)", 0, 0)
        self.criar_card_dashboard(area_cards, "💊", "Medications", f"{medicamentos} upcoming\nschedule(s)", 0, 1)
        self.criar_card_dashboard(area_cards, "📅", "Today's Routine", f"{atividades} registered\nactivity(ies)", 1, 0)
        self.criar_card_dashboard(area_cards, "⚠️", "Occurrences", f"{ocorrencias} recent\nrecord(s)", 1, 1)
        self.criar_card_dashboard(area_cards, "🔔", "Alerts", f"{medicamentos} active\nreminder(s)", 2, 0)
        self.criar_card_dashboard(area_cards, "💬", "Communication", f"{mensagens} registered\nmessage(s)", 2, 1)


        ctk.CTkLabel(
            self.conteudo,
            text="💙 Caring is an act of love.",
            font=("Segoe UI", 20, "bold"),
            text_color=AZUL_MEDIO
        ).pack(pady=(12, 2))

        ctk.CTkLabel(
            self.conteudo,
            text="Technology is the bridge that connects this care every day.",
            font=("Segoe UI", 13),
            text_color=AZUL_ESCURO
        ).pack()

    # ==========================
    # USERS
    # ==========================

    def tela_usuarios(self):
        self.limpar_tela()
        self.criar_titulo("👤 User Registration", "Register, view, or delete elderly people, caregivers, and family members.")

        frame = ctk.CTkFrame(self.conteudo, fg_color=FUNDO_CARD, corner_radius=15)
        frame.pack(pady=8, padx=20, fill="x")

        nome = ctk.CTkEntry(frame, placeholder_text="Name", width=200)
        idade = ctk.CTkEntry(frame, placeholder_text="Age", width=90)
        telefone = ctk.CTkEntry(frame, placeholder_text="Phone", width=150)
        tipo = ctk.CTkComboBox(frame, values=["Elderly", "Caregiver", "Family Member"], width=150)

        nome.grid(row=0, column=0, padx=6, pady=12)
        idade.grid(row=0, column=1, padx=6, pady=12)
        telefone.grid(row=0, column=2, padx=6, pady=12)
        tipo.grid(row=0, column=3, padx=6, pady=12)

        lista = ctk.CTkTextbox(self.conteudo, width=760, height=300)
        lista.pack(pady=10)

        id_delete = ctk.CTkEntry(self.conteudo, placeholder_text="Enter the user ID to delete", width=280)
        id_delete.pack(pady=4)

        def salvar():
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios(nome, idade, telefone, tipo) VALUES (?, ?, ?, ?)",
                (nome.get(), idade.get(), telefone.get(), tipo.get())
            )
            conn.commit()
            conn.close()

            nome.delete(0, "end")
            idade.delete(0, "end")
            telefone.delete(0, "end")
            listar()

        def listar():
            lista.delete("1.0", "end")
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios ORDER BY id DESC")

            for u in cursor.fetchall():
                lista.insert(
                    "end",
                    f"ID {u[0]} | {u[1]}\n\n"
                    f"Age: {u[2]} anos\n\n"
                    f"Phone: {u[3]}\n\n"
                    f"Type: {u[4]}\n\n"
                    f"-----------------------------\n\n"
                )

            conn.close()

        ctk.CTkButton(frame, text="Save User", command=salvar).grid(row=1, column=0, columnspan=4, pady=8)

        ctk.CTkButton(
            self.conteudo,
            text="Delete User",
            fg_color="#B22222",
            hover_color="#8B0000",
            command=lambda: self.deletar_por_id("usuarios", id_delete.get(), listar)
        ).pack(pady=5)

        listar()

    # ==========================
    # MEDICATIONS
    # ==========================

    def tela_medicamentos(self):
        self.limpar_tela()
        self.criar_titulo("💊 Medication Control", "Register, view, or delete medications.")

        frame = ctk.CTkFrame(self.conteudo, fg_color=FUNDO_CARD, corner_radius=15)
        frame.pack(pady=8, padx=20, fill="x")

        nome = ctk.CTkEntry(frame, placeholder_text="Medication", width=160)
        tipo = ctk.CTkEntry(frame, placeholder_text="Type", width=110)
        dose = ctk.CTkEntry(frame, placeholder_text="Dose", width=110)
        horario = ctk.CTkEntry(frame, placeholder_text="Time 08:00", width=120)
        obs = ctk.CTkEntry(frame, placeholder_text="Note", width=180)

        nome.grid(row=0, column=0, padx=5, pady=12)
        tipo.grid(row=0, column=1, padx=5, pady=12)
        dose.grid(row=0, column=2, padx=5, pady=12)
        horario.grid(row=0, column=3, padx=5, pady=12)
        obs.grid(row=0, column=4, padx=5, pady=12)

        lista = ctk.CTkTextbox(self.conteudo, width=780, height=300)
        lista.pack(pady=10)

        id_delete = ctk.CTkEntry(self.conteudo, placeholder_text="Enter the medication ID to delete", width=300)
        id_delete.pack(pady=4)

        def salvar():
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO medicamentos(nome, tipo, dose, horario, observacao) VALUES (?, ?, ?, ?, ?)",
                (nome.get(), tipo.get(), dose.get(), horario.get(), obs.get())
            )
            conn.commit()
            conn.close()

            nome.delete(0, "end")
            tipo.delete(0, "end")
            dose.delete(0, "end")
            horario.delete(0, "end")
            obs.delete(0, "end")
            listar()

        def listar():
            lista.delete("1.0", "end")
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM medicamentos ORDER BY horario")

            for m in cursor.fetchall():
                lista.insert(
                    "end",
                    f"ID {m[0]} | {m[1]}\n\n"
                    f"Type: {m[2]}\n\n"
                    f"Dose: {m[3]}\n\n"
                    f"Time: {m[4]}\n\n"
                    f"Note: {m[5]}\n\n"
                    f"-----------------------------\n\n"
                )

            conn.close()

        ctk.CTkButton(frame, text="Register Medication", command=salvar).grid(row=1, column=0, columnspan=5, pady=8)

        ctk.CTkButton(
            self.conteudo,
            text="Delete Medication",
            fg_color="#B22222",
            hover_color="#8B0000",
            command=lambda: self.deletar_por_id("medicamentos", id_delete.get(), listar)
        ).pack(pady=5)

        listar()

    # ==========================
    # ROUTINE
    # ==========================

    def tela_rotina(self):
        self.limpar_tela()
        self.criar_titulo("📅 Daily Activity Schedule", "Register, complete, or delete activities.")

        frame = ctk.CTkFrame(self.conteudo, fg_color=FUNDO_CARD, corner_radius=15)
        frame.pack(pady=8, padx=20, fill="x")

        descricao = ctk.CTkEntry(frame, placeholder_text="Activity", width=260)
        horario = ctk.CTkEntry(frame, placeholder_text="Time", width=120)
        observacao = ctk.CTkEntry(frame, placeholder_text="Note", width=260)

        descricao.grid(row=0, column=0, padx=6, pady=12)
        horario.grid(row=0, column=1, padx=6, pady=12)
        observacao.grid(row=0, column=2, padx=6, pady=12)

        lista = ctk.CTkTextbox(self.conteudo, width=780, height=270)
        lista.pack(pady=10)

        id_concluir = ctk.CTkEntry(self.conteudo, placeholder_text="Activity ID to mark as completed", width=260)
        id_concluir.pack(pady=3)

        id_delete = ctk.CTkEntry(self.conteudo, placeholder_text="Activity ID to delete", width=260)
        id_delete.pack(pady=3)

        def salvar():
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO atividades(descricao, horario, status, observacao) VALUES (?, ?, ?, ?)",
                (descricao.get(), horario.get(), "Pending", observacao.get())
            )
            conn.commit()
            conn.close()

            descricao.delete(0, "end")
            horario.delete(0, "end")
            observacao.delete(0, "end")
            listar()

        def concluir():
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE atividades SET status='Completed' WHERE id=?", (id_concluir.get(),))
            conn.commit()
            conn.close()

            id_concluir.delete(0, "end")
            listar()

        def listar():
            lista.delete("1.0", "end")
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM atividades ORDER BY horario")

            for a in cursor.fetchall():
                lista.insert(
                    "end",
                    f"ID {a[0]} | {a[1]}\n\n"
                    f"Time: {a[2]}\n\n"
                    f"Status: {a[3]}\n\n"
                    f"Note: {a[4]}\n\n"
                    f"-----------------------------\n\n"
                )

            conn.close()

        ctk.CTkButton(frame, text="Adicionar Activity", command=salvar).grid(row=1, column=0, columnspan=3, pady=8)

        botoes = ctk.CTkFrame(self.conteudo, fg_color=FUNDO)
        botoes.pack(pady=4)

        ctk.CTkButton(botoes, text="Marcar como Completed", command=concluir).grid(row=0, column=0, padx=8)

        ctk.CTkButton(
            botoes,
            text="Deletar Activity",
            fg_color="#B22222",
            hover_color="#8B0000",
            command=lambda: self.deletar_por_id("atividades", id_delete.get(), listar)
        ).grid(row=0, column=1, padx=8)

        listar()

    # ==========================
    # OCCURRENCES
    # ==========================

    def tela_ocorrencias(self):
        self.limpar_tela()
        self.criar_titulo("⚠️ Registro de Occurrences", "Register, view, or delete occurrences.")

        ctk.CTkLabel(
            self.conteudo,
            text="What happened?",
            font=("Segoe UI", 13, "bold"),
            text_color=AZUL_ESCURO
        ).pack(pady=(3, 2))

        descricao = ctk.CTkTextbox(self.conteudo, width=720, height=65)
        descricao.pack(pady=(0, 6))

        gravidade = ctk.CTkComboBox(
            self.conteudo,
            values=["Low", "Medium", "High", "Emergency"],
            width=200
        )
        gravidade.pack(pady=3)

        ctk.CTkLabel(
            self.conteudo,
            text="What solution was applied?",
            font=("Segoe UI", 13, "bold"),
            text_color=AZUL_ESCURO
        ).pack(pady=(8, 2))

        solucao = ctk.CTkTextbox(self.conteudo, width=720, height=65)
        solucao.pack(pady=(0, 6))

        responsavel = ctk.CTkEntry(
            self.conteudo,
            placeholder_text="Person responsible for the action",
            width=320
        )
        responsavel.pack(pady=4)

        lista = ctk.CTkTextbox(self.conteudo, width=800, height=165)
        lista.pack(pady=8)

        id_delete = ctk.CTkEntry(self.conteudo, placeholder_text="Occurrence ID to delete", width=280)
        id_delete.pack(pady=3)

        def salvar():
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO ocorrencias(descricao, gravidade, data, solucao, responsavel)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    descricao.get("1.0", "end").strip(),
                    gravidade.get(),
                    datetime.now().strftime("%d/%m/%Y %H:%M"),
                    solucao.get("1.0", "end").strip(),
                    responsavel.get()
                )
            )
            conn.commit()
            conn.close()

            descricao.delete("1.0", "end")
            solucao.delete("1.0", "end")
            responsavel.delete(0, "end")
            listar()

        def listar():
            lista.delete("1.0", "end")
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, descricao, gravidade, data, solucao, responsavel
                FROM ocorrencias
                ORDER BY id DESC
            """)

            for o in cursor.fetchall():
                lista.insert(
                    "end",
                    f"ID: {o[0]}\n\n"
                    f"Data: {o[3]}\n\n"
                    f"Gravidade: {o[2]}\n\n"
                    f"Occurrence:\n{o[1]}\n\n"
                    f"Applied solution:\n{o[4] if o[4] else 'Not informed'}\n\n"
                    f"Responsible person:\n{o[5] if o[5] else 'Not informed'}\n\n"
                    f"-----------------------------------------\n\n"
                )

            conn.close()

        botoes = ctk.CTkFrame(self.conteudo, fg_color=FUNDO)
        botoes.pack(pady=4)

        ctk.CTkButton(botoes, text="Save Occurrence", command=salvar).grid(row=0, column=0, padx=8)

        ctk.CTkButton(
            botoes,
            text="Delete Occurrence",
            fg_color="#B22222",
            hover_color="#8B0000",
            command=lambda: self.deletar_por_id("ocorrencias", id_delete.get(), listar)
        ).grid(row=0, column=1, padx=8)

        listar()

    # ==========================
    # ALERTS
    # ==========================

    def tela_alertas(self):
        self.limpar_tela()
        self.criar_titulo("🔔 Medication Alerts", "Automatic reminders based on registered medications.")

        lista = ctk.CTkTextbox(self.conteudo, width=800, height=430)
        lista.pack(pady=15)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, tipo, dose, horario FROM medicamentos ORDER BY horario")
        medicamentos = cursor.fetchall()
        conn.close()

        if not medicamentos:
            lista.insert("end", "No medication registered.\n")
        else:
            for m in medicamentos:
                lista.insert(
                    "end",
                    f"🔔 Medication Reminder\n\n"
                    f"Medication: {m[0]}\n\n"
                    f"Type: {m[1]}\n\n"
                    f"Dose: {m[2]}\n\n"
                    f"Time: {m[3]}\n\n"
                    f"-----------------------------\n\n"
                )

    # ==========================
    # DAILY REPORT
    # ==========================

    def tela_relatorio_diario(self):
        self.limpar_tela()
        self.criar_titulo("📄 Daily Report", "Daily summary of patient care.")

        relatorio = ctk.CTkTextbox(self.conteudo, width=800, height=480)
        relatorio.pack(pady=15)

        conn = conectar()
        cursor = conn.cursor()

        relatorio.insert("end", "===== DAILY REPORT =====\n\n\n")

        relatorio.insert("end", "💊 REGISTERED MEDICATIONS\n\n")
        cursor.execute("SELECT nome, dose, horario FROM medicamentos ORDER BY horario")
        for m in cursor.fetchall():
            relatorio.insert("end", f"- {m[0]}\n\nDose: {m[1]}\n\nTime: {m[2]}\n\n")

        relatorio.insert("end", "\n\n📅 ACTIVITIES\n\n")
        cursor.execute("SELECT descricao, horario, status FROM atividades ORDER BY horario")
        for a in cursor.fetchall():
            relatorio.insert("end", f"- {a[0]}\n\nTime: {a[1]}\n\nStatus: {a[2]}\n\n")

        relatorio.insert("end", "\n\n⚠️ OCCURRENCES\n\n")
        cursor.execute("""
            SELECT descricao, gravidade, data, solucao, responsavel
            FROM ocorrencias
            ORDER BY id DESC
        """)
        for o in cursor.fetchall():
            relatorio.insert(
                "end",
                f"Data: {o[2]}\n\n"
                f"Gravidade: {o[1]}\n\n"
                f"Occurrence: {o[0]}\n\n"
                f"Solution: {o[3] if o[3] else 'Not informed'}\n\n"
                f"Responsible person: {o[4] if o[4] else 'Not informed'}\n\n"
                f"-----------------------------\n\n"
            )

        conn.close()

    # ==========================
    # CAREGIVER PANEL
    # ==========================

    def tela_painel_cuidador(self):
        self.limpar_tela()
        self.criar_titulo("🧑‍⚕️ Painel do Caregiver", "Overview of care tasks and pending items.")

        painel = ctk.CTkTextbox(self.conteudo, width=800, height=480)
        painel.pack(pady=15)

        conn = conectar()
        cursor = conn.cursor()

        painel.insert("end", "===== CAREGIVER OVERVIEW =====\n\n\n")

        cursor.execute("SELECT COUNT(*) FROM medicamentos")
        painel.insert("end", f"💊 Total medications: {cursor.fetchone()[0]}\n\n")

        cursor.execute("SELECT COUNT(*) FROM atividades WHERE status IN ('Pending', 'Pendente')")
        painel.insert("end", f"⏰ Pending Activitys: {cursor.fetchone()[0]}\n\n")

        cursor.execute("SELECT COUNT(*) FROM ocorrencias")
        painel.insert("end", f"⚠️ Registered Occurrences: {cursor.fetchone()[0]}\n\n\n")

        painel.insert("end", "PENDING ACTIVITIES\n\n")
        cursor.execute("SELECT descricao, horario FROM atividades WHERE status IN ('Pending', 'Pendente')")
        for a in cursor.fetchall():
            painel.insert("end", f"- {a[0]}\n\nTime: {a[1]}\n\n")

        conn.close()

    # ==========================
    # ELDERLY PANEL
    # ==========================

    def tela_painel_idoso(self):
        self.limpar_tela()
        self.criar_titulo("👴 Painel do Elderly", "Simple screen to view medications and routine.")

        painel = ctk.CTkTextbox(self.conteudo, width=800, height=480)
        painel.pack(pady=15)

        conn = conectar()
        cursor = conn.cursor()

        painel.insert("end", "💊 MY MEDICATIONS TODAY\n\n\n")
        cursor.execute("SELECT nome, dose, horario FROM medicamentos ORDER BY horario")
        for m in cursor.fetchall():
            painel.insert("end", f"🔔 {m[0]}\n\nDose: {m[1]}\n\nTime: {m[2]}\n\n")

        painel.insert("end", "\n\n📅 MY ROUTINE\n\n\n")
        cursor.execute("SELECT descricao, horario, status FROM atividades ORDER BY horario")
        for a in cursor.fetchall():
            painel.insert("end", f"- {a[0]}\n\nTime: {a[1]}\n\nStatus: {a[2]}\n\n")

        painel.insert("end", "\n\n🆘 In case of emergency, notify the caregiver or family member.\n")

        conn.close()

    # ==========================
    # COMMUNICATION
    # ==========================

    def tela_comunicacao(self):
        self.limpar_tela()
        self.criar_titulo("💬 Caregiver and Family Communication", "Register simple messages between caregiver and family.")

        remetente = ctk.CTkComboBox(
            self.conteudo,
            values=["Caregiver", "Family Member"],
            width=200
        )
        remetente.pack(pady=5)

        mensagem = ctk.CTkEntry(
            self.conteudo,
            placeholder_text="Type the message",
            width=560
        )
        mensagem.pack(pady=8)

        chat = ctk.CTkTextbox(self.conteudo, width=800, height=360)
        chat.pack(pady=12)

        def enviar():
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO mensagens(remetente, mensagem, data) VALUES (?, ?, ?)",
                (remetente.get(), mensagem.get(), datetime.now().strftime("%d/%m/%Y %H:%M"))
            )
            conn.commit()
            conn.close()

            mensagem.delete(0, "end")
            listar()

        def listar():
            chat.delete("1.0", "end")

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT remetente, mensagem, data FROM mensagens ORDER BY id DESC")

            for m in cursor.fetchall():
                chat.insert(
                    "end",
                    f"Date: {m[2]}\n\nSender: {m[0]}\n\nMessage: {m[1]}\n\n-----------------------------\n\n"
                )

            conn.close()

        ctk.CTkButton(self.conteudo, text="Send Message", command=enviar).pack(pady=4)

        listar()

    # ==========================
    # FINAL REPORT
    # ==========================

    def tela_relatorio_final(self):
        self.limpar_tela()
        self.criar_titulo("📊 Final Report", "Summary of tasks, pending items, medications, and important notes.")

        relatorio = ctk.CTkTextbox(self.conteudo, width=800, height=480)
        relatorio.pack(pady=15)

        conn = conectar()
        cursor = conn.cursor()

        relatorio.insert("end", "===== PATIENT FINAL REPORT =====\n\n\n")

        relatorio.insert("end", "✅ COMPLETED TASKS\n\n")
        cursor.execute("SELECT descricao, horario FROM atividades WHERE status IN ('Completed', 'Concluída')")
        concluidas = cursor.fetchall()

        if concluidas:
            for a in concluidas:
                relatorio.insert("end", f"- {a[0]}\n\nTime: {a[1]}\n\n")
        else:
            relatorio.insert("end", "- No completed task.\n\n")

        relatorio.insert("end", "\n\n⏰ PENDING TASKS\n\n")
        cursor.execute("SELECT descricao, horario FROM atividades WHERE status IN ('Pending', 'Pendente')")
        pendentes = cursor.fetchall()

        if pendentes:
            for a in pendentes:
                relatorio.insert("end", f"- {a[0]}\n\nTime: {a[1]}\n\n")
        else:
            relatorio.insert("end", "- No pending task.\n\n")

        relatorio.insert("end", "\n\n💊 REGISTERED MEDICATIONS\n\n")
        cursor.execute("SELECT nome, dose, horario FROM medicamentos ORDER BY horario")
        medicamentos = cursor.fetchall()

        if medicamentos:
            for m in medicamentos:
                relatorio.insert("end", f"- {m[0]}\n\nDose: {m[1]}\n\nTime: {m[2]}\n\n")
        else:
            relatorio.insert("end", "- No medication registered.\n\n")

        relatorio.insert("end", "\n\n⚠️ IMPORTANT NOTES AND OCCURRENCES\n\n")
        cursor.execute("""
            SELECT descricao, gravidade, data, solucao, responsavel
            FROM ocorrencias
            ORDER BY id DESC
        """)
        ocorrencias = cursor.fetchall()

        if ocorrencias:
            for o in ocorrencias:
                relatorio.insert(
                    "end",
                    f"Data: {o[2]}\n\n"
                    f"Gravidade: {o[1]}\n\n"
                    f"Occurrence:\n{o[0]}\n\n"
                    f"Applied solution:\n{o[3] if o[3] else 'Not informed'}\n\n"
                    f"Responsible person:\n{o[4] if o[4] else 'Not informed'}\n\n"
                    f"-----------------------------\n\n"
                )
        else:
            relatorio.insert("end", "- No occurrence registered.\n\n")

        conn.close()


if __name__ == "__main__":
    app = SistemaCuidados()
    app.mainloop()
