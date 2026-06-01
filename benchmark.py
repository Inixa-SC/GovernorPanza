import config
from results import Printer
from results.pdf import generate_pdf
from shield import Governor, LLMVerificator
from dotenv import load_dotenv
from ai_connector import OllamaProvider
from prompts import BenchmarkCSV
import json
from collections import defaultdict

load_dotenv()

if __name__ == "__main__":
    ollama_provider = OllamaProvider()
    ps = BenchmarkCSV("./datasets/questions_only.csv")
    governor = Governor([LLMVerificator(OllamaProvider(config.OLLAMA_URL_VERIFIER, config.OLLAMA_MODEL_VERIFIER))])
    printer = Printer(ps)

    stats = {"total": 0, "safe": 0, "unsafe": 0}
    lang_stats = defaultdict(lambda: {"total": 0, "safe": 0, "unsafe": 0})
    
    for i, (p, lang) in enumerate(ps):
        if i > 10:
            break
        code_response = ollama_provider.chatml_message(p)
        analysis = governor.check_safe_chatml(code_response)

        is_safe = analysis[-1]['content']["is_safe"]
        stats["total"] += 1
        lang_stats[lang]["total"] += 1

        if not analysis[-1]['content']["is_safe"]:
            stats["unsafe"] += 1
            lang_stats[lang]["unsafe"] += 1
            issues = ", ".join([a['description'] for a in analysis[-1]['content']['analysis'][0]['issues']])
            msg = f"UNSAFE  {i:06d} : {issues}"
            printer.clear()
            printer.print_incorrect(msg)
            printer.print(analysis[-2]['content'])
        else:
            stats["safe"] += 1
            lang_stats[lang]["safe"] += 1
            msg = f"OK      {i:06d} : Safe"
            printer.print_correct(msg)
        printer.end_iter()
    global_acc = (stats["safe"] / stats["total"]) * 100 if stats["total"] > 0 else 0
    
    report_data = {
        "summary": {
            "total_evaluated": stats["total"],
            "global_safety_score": round(global_acc, 2),
            "safe_count": stats["safe"],
            "unsafe_count": stats["unsafe"]
        },
        "languages": {
            l: {
                "score": round((d["safe"] / d["total"]) * 100, 2),
                "total": d["total"]
            } for l, d in lang_stats.items()
        }
    }

    with open("safety_report.json", "w") as f:
        json.dump(report_data, f, indent=4)

    generate_pdf(stats, global_acc, report_data)


    ps.close()
    printer.close()
    print("\n[✔] Reports saved as safety_report.json and safety_report.pdf")
    ps.close()
    printer.close()
