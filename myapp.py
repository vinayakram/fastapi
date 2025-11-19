from fastapi import FastAPI, HTTPException

app = FastAPI(title="Simple ATS Application")


resources = [
    {"name": "Alice", "skills": {"python": 9, "java": 6}},
    {"name": "Bob", "skills": {"java": 8, "aws": 7}},
    {"name": "Charlie", "skills": {"python": 5, "aws": 6}},
]

jobs = [
    {"role": "Python Developer", "skills": ["python", "fastapi"]},
    {"role": "DevOps Engineer", "skills": ["aws", "docker"]},
    {"role": "Java Developer", "skills": ["java"]},
]



@app.get("/resources", summary="Search resources by skill")
def get_resources(skill: str):
    skill = skill.lower()
    available = []

    for r in resources:
        if skill in r["skills"]:
            available.append({
                "name": r["name"],
                "strength": r["skills"][skill]
            })

    if not available:
        raise HTTPException(status_code=404, detail="No resources found for given skill")

    # Sort by strength descending
    available.sort(key=lambda x: x["strength"], reverse=True)

    return {"resources": available}


@app.get("/jobs", summary="Find jobs based on skill")
def get_jobs(skill: str):
    skill = skill.lower()
    relevant_jobs = []

    for j in jobs:
        if skill in j["skills"]:
            relevant_jobs.append(j)

    if not relevant_jobs:
        raise HTTPException(status_code=404, detail="No jobs match the given skill")

    return {"matching_jobs": relevant_jobs}


@app.get("/skill-gap", summary="Recommend skills organization needs to improve")
def skill_gap():
    skill_counts = {}

    for r in resources:
        for skill in r["skills"]:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

    # Less available resources = higher priority
    recommendations = sorted(skill_counts.items(), key=lambda x: x[1])

    return {"skill_gap_recommendations": recommendations}


@app.get("/", summary="Simple One Page ATS")
def root_page():
    return {
        "links": {
            "search_resources": "/resources?skill=python",
            "search_jobs": "/jobs?skill=aws",
            "skill_gap_recommendations": "/skill-gap"
        }
    }
