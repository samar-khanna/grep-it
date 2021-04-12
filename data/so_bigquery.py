from google.cloud import bigquery

# Create a "Client" object
client = bigquery.Client()

# Construct a reference to the "stackoverflow" dataset
dataset_ref = client.dataset("stackoverflow", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

questions_table_id = "bigquery-public-data.stackoverflow.posts_questions"
answers_table_id = "bigquery-public-data.stackoverflow.posts_answers"

cols = [
    "id",
    "title",
    "body",
    "accepted_answer_id",
    "answer_count",
    "comment_count",
    "community_owned_date",
    "creation_date",
    "favorite_count",
    "last_activity_date",
    "last_edit_date",
    "last_editor_display_name",
    "last_editor_user_id",
    "owner_display_name",
    "owner_user_id",
    "parent_id",
    "post_type_id",
    "score",
    "tags",
    "view_count",
]

cols_select = lambda t: ",".join([f"{t}.{col} as {t}_{col}" for col in cols])

python_qna_table_id = "grep-it.stackoverflow.python_qna"
job_config = bigquery.QueryJobConfig(destination=python_qna_table_id)

# Add "LIMIT <num_rows> at the end if want to get a smaller dataset
# Saved ~200000 rows in grep-it.stackoverflow.python_qna already
# Saved 10000 rows in grep-it.stackoverflow.python_qna_small already
query = f"""
    SELECT 
        {cols_select("q")}, {cols_select("a")}
    FROM `{answers_table_id}` AS a 
        INNER JOIN   `{questions_table_id}` AS q 
    ON q.id = a.parent_id AND q.tags = 'python'
"""
print(query)
query_job = client.query(query, job_config=job_config)
query_job.result() 
print("Query results loaded to the table {}".format(python_qna_table_id))
