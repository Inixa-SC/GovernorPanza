from fpdf import FPDF

def generate_pdf(stats, global_acc, report_data):
    pdf = FPDF()
    pdf.add_page()
    
    # --- UI Theme: Deep Charcoal & Electric Cyan ---
    # Background
    pdf.set_fill_color(18, 18, 18) # Deep matte black
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Header Section
    pdf.set_font("Courier", "B", 22)
    pdf.set_text_color(0, 210, 255) # Electric Cyan
    pdf.cell(0, 25, "// SAFETY_BENCHMARK_REPORT", ln=True, align="L")
    
    # Metric "Cards" (Modern Legible Styling)
    pdf.set_fill_color(30, 30, 30) # Dark grey card
    pdf.rect(10, 35, 190, 35, 'F') 
    
    # Score Label
    pdf.set_xy(15, 40)
    pdf.set_font("Courier", "B", 14)
    pdf.set_text_color(255, 255, 255) # Clean White
    pdf.cell(0, 10, f"SYSTEM ACCURACY: {global_acc:.2f}%")
    
    # Sub-stats with a soft grey
    pdf.set_xy(15, 52)
    pdf.set_font("Courier", "", 11)
    pdf.set_text_color(180, 180, 180) 
    pdf.cell(0, 10, f"PROCESSED: {stats['total']} prompts | SAFE: {stats['safe']} | UNSAFE: {stats['unsafe']}")

    pdf.ln(25)

    # --- Data Grid ---
    # Header Row
    pdf.set_font("Courier", "B", 11)
    pdf.set_fill_color(45, 45, 45) # Slightly lighter header
    pdf.set_text_color(0, 210, 255)
    
    # Table borders: very subtle
    pdf.set_draw_color(60, 60, 60)
    pdf.cell(70, 12, " [ LANGUAGE ]", border=1, fill=True)
    pdf.cell(60, 12, " [ SCORE ]", border=1, fill=True)
    pdf.cell(60, 12, " [ VOLUME ]", border=1, fill=True, ln=True)

    # Data Rows (White text for high legibility)
    pdf.set_text_color(240, 240, 240)
    pdf.set_font("Courier", "", 11)
    
    for lang, data in report_data["languages"].items():
        # High contrast white on dark
        pdf.cell(70, 10, f" {lang}", border=1)
        pdf.cell(60, 10, f" {data['score']:.1f}%", border=1)
        pdf.cell(60, 10, f" {data['total']}", border=1, ln=True)

    # Footer
    pdf.set_y(-20)
    pdf.set_font("Courier", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "STRICTLY_CONFIDENTIAL // VER_1.0.4", align="R")

    pdf.output("safety_report.pdf")
