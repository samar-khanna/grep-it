## StackOverflow Dataset

Download the datasets from: [Google Drive](https://drive.google.com/drive/u/1/folders/1xaIJ9KXoiK8d_CHUQ50NPBSk3I1o7MaP)

In the Public BigQuery StackOverflow dataset the available tables are:
- badges
- comments
- post_history
- post_links
- posts_answers
- posts_moderator_nomination
- posts_orphaned_tag_wiki
- posts_privilege_wiki
- posts_questions
- posts_tag_wiki
- posts_tag_wiki_excerpt
- posts_wiki_placeholder
- stackoverflow_posts
- tags
- users
- votes


### posts_questions
Table schema:
| Name                     |   Type    |
| :----------------------- | :-------: |
| id                       |  INTEGER  |
| title                    |  STRING   |
| body                     |  STRING   |
| accepted_answer_id       |  INTEGER  |
| answer_count             |  INTEGER  |
| comment_count            |  INTEGER  |
| community_owned_date     | TIMESTAMP |
| creation_date            | TIMESTAMP |
| favorite_count           |  INTEGER  |
| last_activity_date       | TIMESTAMP |
| last_edit_date           | TIMESTAMP |
| last_editor_display_name |  STRING   |
| last_editor_user_id      |  INTEGER  |
| owner_display_name       |  STRING   |
| owner_user_id            |  INTEGER  |
| parent_id                |  STRING   |
| post_type_id             |  INTEGER  |
| score                    |  INTEGER  |
| tags                     |  STRING   |
| view_count               |  INTEGER  |

Total # of rows: 20,890,054

### posts_answers
Table schema:
| Name                     |   Type    |
| :----------------------- | :-------: |
| id                       |  INTEGER  |
| title                    |  STRING   |
| body                     |  STRING   |
| accepted_answer_id       |  INTEGER  |
| answer_count             |  INTEGER  |
| comment_count            |  INTEGER  |
| community_owned_date     | TIMESTAMP |
| creation_date            | TIMESTAMP |
| favorite_count           |  INTEGER  |
| last_activity_date       | TIMESTAMP |
| last_edit_date           | TIMESTAMP |
| last_editor_display_name |  STRING   |
| last_editor_user_id      |  INTEGER  |
| owner_display_name       |  STRING   |
| owner_user_id            |  INTEGER  |
| parent_id                |  STRING   |
| post_type_id             |  INTEGER  |
| score                    |  INTEGER  |
| tags                     |  STRING   |
| view_count               |  INTEGER  |
Total # of rows: 31,169,429

## Statistics
The total number of `post_questions` with tag `python`: 109091