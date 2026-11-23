import random
import streamlit as st

st.set_page_config(
    page_title="Minesweeper 10x10", page_icon="💣", layout="centered"
)

# ==========================================
# CSS KHUSUS AGAR TAMPILAN & WARNA SAMA PERSIS DENGAN PYGAME
# ==========================================
st.markdown(
    """
<style>
    /* Latar belakang utama gelap seperti Pygame (30, 30, 40) */
    .stApp {
        background-color: #1E1E28;
        color: #FFFFFF;
    }
    /* Mengatur jarak antar kolom kotak agar rapat seperti di Pygame */
    div[data-testid="stHorizontalBlock"] {
        gap: 4px !important;
        margin-bottom: -12px !important;
    }
    /* Gaya dasar setiap kotak tombol */
    div[data-testid="stButton"] > button {
        height: 44px !important;
        min-height: 44px !important;
        padding: 0px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 6px !important;
        border: none !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 1. PENGATURAN & DATA GAME (OTAK GAME)
# Sama persis dengan versi Pygame!
# ==========================================
UKURAN = 10
JUMLAH_BOM = 12


def mulai_ulang():
  papan_rahasia = [[0 for _ in range(UKURAN)] for _ in range(UKURAN)]
  papan_layar = [["#" for _ in range(UKURAN)] for _ in range(UKURAN)]

  bom_terpasang = 0
  while bom_terpasang < JUMLAH_BOM:
    baris = random.randint(0, UKURAN - 1)
    kolom = random.randint(0, UKURAN - 1)
    if papan_rahasia[baris][kolom] != "B":
      papan_rahasia[baris][kolom] = "B"
      bom_terpasang += 1

  for r in range(UKURAN):
    for c in range(UKURAN):
      if papan_rahasia[r][c] == "B":
        continue

      jumlah_bom_sekitar = 0
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          nr, nc = r + dr, c + dc
          if 0 <= nr < UKURAN and 0 <= nc < UKURAN:
            if papan_rahasia[nr][nc] == "B":
              jumlah_bom_sekitar += 1
      papan_rahasia[r][c] = jumlah_bom_sekitar

  st.session_state.papan_rahasia = papan_rahasia
  st.session_state.papan_layar = papan_layar
  st.session_state.status_game = "MAIN"


if "papan_layar" not in st.session_state:
  mulai_ulang()


# ==========================================
# 2. FUNGSI LOGIKA AKSI PEMAIN
# ==========================================
def hitung_bendera():
  jumlah = 0
  for r in range(UKURAN):
    for c in range(UKURAN):
      if st.session_state.papan_layar[r][c] == "F":
        jumlah += 1
  return jumlah


def buka_semua_bom():
  for i in range(UKURAN):
    for j in range(UKURAN):
      if st.session_state.papan_rahasia[i][j] == "B":
        st.session_state.papan_layar[i][j] = "*"


def cek_menang_otomatis():
  kotak_tertutup = 0
  for r in range(UKURAN):
    for c in range(UKURAN):
      isi = st.session_state.papan_layar[r][c]
      if isi == "#" or isi == "F":
        kotak_tertutup += 1

  if kotak_tertutup == JUMLAH_BOM:
    st.session_state.status_game = "MENANG"


def cek_jawaban_akhir():
  if st.session_state.status_game != "MAIN":
    return

  semua_benar = True
  for r in range(UKURAN):
    for c in range(UKURAN):
      if (
          st.session_state.papan_rahasia[r][c] == "B"
          and st.session_state.papan_layar[r][c] != "F"
      ):
        semua_benar = False
      elif (
          st.session_state.papan_rahasia[r][c] != "B"
          and st.session_state.papan_layar[r][c] == "F"
      ):
        semua_benar = False

  if semua_benar:
    st.session_state.status_game = "MENANG"
  else:
    st.session_state.status_game = "KALAH"
    buka_semua_bom()


def buka_otomatis_kosong(r, c):
  antrean = [(r, c)]
  layar = st.session_state.papan_layar
  rahasia = st.session_state.papan_rahasia

  while len(antrean) > 0:
    baris_sekarang, kolom_sekarang = antrean.pop(0)

    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        nr = baris_sekarang + dr
        nc = kolom_sekarang + dc

        if 0 <= nr < UKURAN and 0 <= nc < UKURAN:
          if layar[nr][nc] == "#":
            nilai = rahasia[nr][nc]
            if nilai == 0:
              layar[nr][nc] = ""
              antrean.append((nr, nc))
            elif nilai != "B":
              layar[nr][nc] = str(nilai)


def klik_kotak(r, c, mode_bendera):
  if st.session_state.status_game != "MAIN":
    return

  layar = st.session_state.papan_layar
  rahasia = st.session_state.papan_rahasia

  if mode_bendera:
    if layar[r][c] == "#":
      layar[r][c] = "F"
    elif layar[r][c] == "F":
      layar[r][c] = "#"
  else:
    if layar[r][c] != "#":
      return

    if rahasia[r][c] == "B":
      st.session_state.status_game = "KALAH"
      buka_semua_bom()
    else:
      nilai = rahasia[r][c]
      if nilai == 0:
        layar[r][c] = ""
        buka_otomatis_kosong(r, c)
      else:
        layar[r][c] = str(nilai)

      cek_menang_otomatis()


# ==========================================
# 3. TAMPILAN WEB STREAMLIT (MIRIP PYGAME)
# ==========================================
sisa_bom = JUMLAH_BOM - hitung_bendera()

# Teks Status di Bagian Atas Layar (Sama persis dengan Pygame)
if st.session_state.status_game == "MAIN":
  st.markdown(
      "<h4 style='text-align: center; color: #FFFFFF;'>Sisa Bom:"
      f" {sisa_bom}</h4>",
      unsafe_allow_html=True,
  )
elif st.session_state.status_game == "KALAH":
  st.markdown(
      "<h4 style='text-align: center; color: #DC3C3C;'>KAMU KALAH! Ada bom"
      " yang terlewat atau salah tandai!</h4>",
      unsafe_allow_html=True,
  )
elif st.session_state.status_game == "MENANG":
  st.markdown(
      "<h4 style='text-align: center; color: #50DC64;'>KAMU MENANG! Semua"
      " posisi bom tepat!</h4>",
      unsafe_allow_html=True,
  )

# Toggle pengganti Klik Kanan untuk pasang bendera
mode_bendera = st.toggle("🚩 Mode Pasang Bendera (Pengganti Klik Kanan)")

# Menggambar Papan Kotak 10x10 dan Pewarnaan Tiap Kotak
css_warna_kotak = "<style>"

for r in range(UKURAN):
  kolom_ui = st.columns(UKURAN)
  for c in range(UKURAN):
    isi = st.session_state.papan_layar[r][c]

    # Menentukan label dan warna kotak agar sama persis dengan Pygame
    if isi == "#":
      label_tombol = " "
      warna_bg = "#465064"  # WARNA_TERTUTUP (70, 80, 100)
      warna_teks = "#14141E"
    elif isi == "F":
      label_tombol = "F"
      warna_bg = "#F0B428"  # WARNA_BENDERA (240, 180, 40)
      warna_teks = "#14141E"
    elif isi == "*":
      label_tombol = "*"
      warna_bg = "#DC3C3C"  # WARNA_BOM (220, 60, 60)
      warna_teks = "#14141E"
    else:
      label_tombol = isi if isi != "" else " "
      warna_bg = "#D2D7E1"  # WARNA_TERBUKA (210, 215, 225)
      warna_teks = "#14141E"

    key_btn = f"btn_{r}_{c}"
    # Menyuntikkan warna ke masing-masing kotak berdasarkan key tombolnya
    css_warna_kotak += f"""
        div.st-key-{key_btn} button {{
            background-color: {warna_bg} !important;
            color: {warna_teks} !important;
        }}
        """

    with kolom_ui[c]:
      st.button(
          label=label_tombol,
          key=key_btn,
          use_container_width=True,
          on_click=klik_kotak,
          args=(r, c, mode_bendera),
      )

# Tombol Bawah ("CEK JAWABAN" & "MAIN LAGI") dengan warna yang sama
st.write("")
col_cek, col_ulang = st.columns(2)

css_warna_kotak += """
div.st-key-btn_cek button {
    background-color: #3296DC !important;
    color: #FFFFFF !important;
}
div.st-key-btn_ulang button {
    background-color: #50B464 !important;
    color: #FFFFFF !important;
}
</style>
"""
st.markdown(css_warna_kotak, unsafe_allow_html=True)

with col_cek:
  st.button(
      "CEK JAWABAN",
      key="btn_cek",
      use_container_width=True,
      on_click=cek_jawaban_akhir,
  )

with col_ulang:
  st.button(
      "MAIN LAGI", key="btn_ulang", use_container_width=True, on_click=mulai_ulang
  )
