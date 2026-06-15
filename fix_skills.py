import json, os, time, requests, sys

JULES_API = "https://jules.googleapis.com/v1alpha"
HEADERS = {
    "X-Goog-Api-Key": os.environ.get("JULES_API_KEY", ""),
    "Content-Type": "application/json",
}

def build_prompt(report: dict) -> str:
    findings = report["filtered_findings"]
    by_sev = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    findings = sorted(findings, key=lambda x: by_sev[x["severity"]])

    lines = [
        f"SkillSpector security scan: score {report['risk_score']}/100 "
        f"({report['risk_severity']}) — {report['risk_recommendation']}.",
        f"{len(findings)} issue(s) found. Fix each one. Do NOT refactor unrelated code.",
        "",
    ]
    for f in findings:
        lines += [
            f"[{f['severity']}] {f['rule_id']} — {f['message']}",
            f"  Location: {f.get('location', 'unknown')}",
            f"  {f.get('explanation', '')}",
            "",
        ]
    lines.append(
        "After fixing, the codebase should pass: "
        "`skillspector scan . --no-llm` with a score below 20."
    )
    return "\n".join(lines)

def process_report(report_path):
    # Load report
    try:
        with open(report_path) as f:
            report = json.load(f)
    except Exception as e:
        print(f"Error loading {report_path}: {e}")
        return

    if not report.get("filtered_findings"):
        print(f"Scan clean for {report_path} — no Jules task needed.")
        return

    # Resolve source (repo must have Jules GitHub App installed)
    try:
        resp = requests.get(f"{JULES_API}/sources", headers=HEADERS)
        resp.raise_for_status()
        sources = resp.json()
    except Exception as e:
        print(f"Error fetching sources: {e}")
        return

    if not sources.get("sources"):
        print("No Jules sources found. Install the Jules GitHub App on your repo first.")
        return

    # Resolve source name
    repo_slug = os.environ.get("GITHUB_REPOSITORY", "")
    source_name = next(
        (s["name"] for s in sources["sources"] if repo_slug in s["name"]),
        sources["sources"][0]["name"]
    )
    print(f"Using source: {source_name} for {report_path}")

    # Create Jules session
    payload = {
        "title": f"[SkillSpector] Fix {report['risk_severity']} issues (score {report['risk_score']}/100)",
        "prompt": build_prompt(report),
        "sourceContext": {
            "source": source_name,
            "githubRepoContext": {"startingBranch": "main"},
        },
        "automationMode": "AUTO_CREATE_PR",
    }
    try:
        session = requests.post(f"{JULES_API}/sessions", headers=HEADERS, json=payload).json()
        session_id = session["id"]
        print(f"Jules session started for {report_path}: {session_id}")
    except Exception as e:
        print(f"Error creating session: {e}")
        return

    # Poll for PR (max ~7.5 min)
    for i in range(30):
        time.sleep(15)
        try:
            s = requests.get(f"{JULES_API}/sessions/{session_id}", headers=HEADERS).json()
            for out in s.get("outputs", []):
                if "pullRequest" in out:
                    pr = out["pullRequest"]
                    print(f"✅ PR ready for {report_path}: {pr['url']}")
                    return

            activities = requests.get(
                f"{JULES_API}/sessions/{session_id}/activities?pageSize=5",
                headers=HEADERS
            ).json().get("activities", [])
            if activities:
                last = activities[-1].get("progressUpdated", {}).get("title", "…")
                print(f"[{i+1}/30] {report_path} Jules: {last}")
        except Exception as e:
            print(f"Error polling session: {e}")

    print(f"Timed out for {report_path} — check https://jules.google.com for status.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_skills.py <report.json> or <reports_dir>")
        sys.exit(1)

    path = sys.argv[1]
    if os.path.isdir(path):
        for f in os.listdir(path):
            if f.endswith(".json"):
                process_report(os.path.join(path, f))
    else:
        process_report(path)
