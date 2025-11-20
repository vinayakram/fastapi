from fastapi import FastAPI, HTTPException

app = FastAPI(title="ATS Application")


#resources and jobs list
resources = [
    {"name": "vinayak", "skills": {"python": 9, "java": 6,"sql":6}},
    {"name": "vyanktesh", "skills": {"java": 8, "aws": 7}},
    {"name": "Harish", "skills": {"python": 5, "aws": 6}},
]

jobs = [
    {"role": "Python Developer", "skills": ["python", "fastapi"]},
    {"role": "DevOps Engineer", "skills": ["aws", "docker"]},
    {"role": "Java Developer", "skills": ["java"]},
]


#listing resources based on skill
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

    
    available.sort(key=lambda x: x["strength"], reverse=True)

    return {"resources": available}

#List jobs based on skill
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

#skill gap recommondation to organization
@app.get("/skill-gap", summary="Recommend skills organization needs to improve")
def skill_gap():
    
    skill_counts = {}
    for r in resources:
        for skill in r["skills"]:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

    
    required_skills = set()
    for job in jobs:
        for skill in job["skills"]:
            required_skills.add(skill.lower())

    
    recommendations = []
    
    for skill in required_skills:
        count = skill_counts.get(skill, 0)
        priority = "CRITICAL" if count == 0 else "LOW"
        if count == 0:
            priority = "CRITICAL (missing entirely)"
        elif count == 1:
            priority = "HIGH (only 1 person)"
        elif count == 2:
            priority = "MEDIUM"
        else:
            priority = "LOW"
            
        recommendations.append({
            "skill": skill,
            "people_with_skill": count,
            "priority": priority,
            "urgency_score": 100 - (count * 30)  
        })

    
    recommendations.sort(key=lambda x: x["urgency_score"], reverse=True)

    return {
        "message": "Skills your team is missing or weak in (for current job openings)",
        "skill_gap_recommendations": recommendations
    }


#root page
@app.get("/", summary="ATS")
def root_page():
    return {
        "links": {
            "search_resources": "/resources?skill=python",
            "search_jobs": "/jobs?skill=aws",
            "skill_gap_recommendations": "/skill-gap"
        }
    }
