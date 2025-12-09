import pandas as pd
import asyncio
from routers.job_review import review_job, JobDescriptionInput

async def run_eval():
    df = pd.read_csv("job_descriptions_synthetic.csv")

    summaries = []
    fixed_descriptions = []

    for row in df.itertuples():
        input_text = row[1]

        # Call your async function PROPERLY
        result = await review_job(JobDescriptionInput(job_description=input_text))

        summaries.append(result["summary"])
        fixed_descriptions.append(result["fixed"])

    df["Summary"] = summaries
    df["Fixed Description"] = fixed_descriptions

    df.to_csv("eval_output_new.csv", index=False)
    print("✅ Done! Output written to eval_output.csv")

if __name__ == "__main__":
    asyncio.run(run_eval())
