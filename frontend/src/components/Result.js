import { Component } from "react";
import styles from '../styles/Result.module.css';

class Result extends Component {
    constructor(props) {
        super(props)

        this.state = {
            answer: undefined
        };
    }

    componentDidMount() {
        this.getGitHubData();
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevProps.blob_id !== this.props.blob_id) this.getGitHubData();
    }

    getGitHubData = () => {
        if (this.props.type === "gh") {
            fetch(`https://api.github.com/repos/${this.props.repo_name}/git/blobs/${this.props.blob_id}`, {
                method: "GET",
                headers: {
                    "Accept": "application/vnd.github.v3+json",
                    "Authorization": `Basic ${btoa("LucaKoval")}`
                },
            })
            .then(res => {
                res.json().then(data => {
                    if (res.status === 200) {
                        let answer = `<pre><code>${atob(data.content)}</code></pre>`
                        this.setState({ answer: answer })
                    }
                })
            })
        }
    }

    render() {
        if (this.props.type === "so") {
            return (
                <div className={styles.container}>
                    <div className={styles.questionContainer}>
                        <div className="bold">Question:&nbsp;</div>
                        <a className={styles.value} href={this.props.url}>{this.props.title}</a>
                    </div>
                    <div className={styles.questionContainer}>
                        <div className="bold">Answer Upvote Score:&nbsp;</div>
                        <div className={styles.value}>{this.props.upvoteScore}</div>
                    </div>
                    <div className={styles.answerContainer}>
                        <div className="bold">Answer:</div>
                        <div
                            className={styles.answer}
                            dangerouslySetInnerHTML={{
                                __html: this.props.answer
                            }}
                        />
                    </div>
                </div>
            )
        } else {
            let answer = this.state.answer === undefined ? "<div>Loading...</div>" : this.state.answer;
            return (
                <div className={styles.container}>
                    <div className={styles.questionContainer}>
                        <div className="bold">Repository:&nbsp;</div>
                        <a className={styles.value} href={this.props.repo_link}>{this.props.repo_name}</a>
                    </div>
                    <div className={styles.questionContainer}>
                        <div className="bold">File:&nbsp;</div>
                        <div className={styles.value}>{this.props.filepath}</div>
                    </div>
                    <div className={styles.questionContainer}>
                        <div className="bold">Answer Star Score:&nbsp;</div>
                        <div className={styles.value}>{this.props.stars}</div>
                    </div>
                    <div className={styles.answerContainer}>
                        <div className="bold">Answer:</div>
                        <div
                            className={styles.answer}
                            id={styles.ghAnswer}
                            dangerouslySetInnerHTML={{
                                __html: answer
                            }}
                        />
                    </div>
                </div>
            )
        }
    }
}

export default Result;