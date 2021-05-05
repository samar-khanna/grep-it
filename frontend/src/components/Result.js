import { Component } from "react";
import styles from '../styles/Result.module.css';

class Result extends Component {
    constructor(props) {
        super(props)

        this.state = {
            answer: undefined,
            minimized: true,
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
        const arrow = () => {
            if (this.state.minimized) {
                return (
                    <svg width="14" height="8" className={styles.arrow} >
                        <line x1="2" y1="2" x2="7" y2="7" />
                        <line x1="12" y1="2" x2="7" y2="7" />
                        <circle cx="7" cy="7" r="1" />
                    </svg>
                )
            } else {
                return (
                    <svg width="14" height="8" className={styles.arrow} >
                        <line x1="2" y1="7" x2="7" y2="2" />
                        <line x1="12" y1="7" x2="7" y2="2" />
                        <circle cx="7" cy="2" r="1" />
                    </svg>
                )
            }
        }
        if (this.props.type === "so") {
            return (
                <div className={styles.minimized} style={this.state.minimized ? { height: "300px" } : { height: "max-content", paddingBottom: "64px" }} >
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
                    <div
                        onClick={() => this.setState({ minimized: !this.state.minimized })}
                        className={styles.expandContainer}
                        style={this.state.minimized ? { top: "calc(300px - 64px)", boxShadow: "0px -2px 40px rgba(0, 0, 0, 0.4)" } : { bottom: "0px" }}
                    >
                        {arrow()}
                        <div>{this.state.minimized ? "Expand" : "Minimize"}</div>
                        {arrow()}
                    </div>
                </div>
            )
        } else {
            let answer = this.state.answer === undefined ? "<div>Loading...</div>" : this.state.answer;
            return (
                <div className={styles.minimized} style={this.state.minimized ? { height: "300px" } : { height: "max-content", paddingBottom: "64px" }} >
                    <div className={styles.container}> 
                        <div className={styles.questionContainer}>
                            <div className="bold">Repository:&nbsp;</div>
                            <a className={styles.ghValue} href={this.props.repo_link}>{this.props.repo_name}</a>
                        </div>
                        <div className={styles.questionContainer}>
                            <div className="bold">File:&nbsp;</div>
                            <div className={styles.ghValue}>{this.props.filepath}</div>
                        </div>
                        <div className={styles.questionContainer}>
                            <div className="bold">Answer Star Score:&nbsp;</div>
                            <div>{this.props.stars}</div>
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
                    <div
                        onClick={() => this.setState({ minimized: !this.state.minimized })}
                        className={styles.expandContainer}
                        style={this.state.minimized ? { top: "calc(300px - 64px)", boxShadow: "0px -2px 40px rgba(0, 0, 0, 0.4)" } : { bottom: "0px" }}
                    >
                        {arrow()}
                        <div>{this.state.minimized ? "Expand" : "Minimize"}</div>
                        {arrow()}
                    </div>
                </div>
            )
        }
    }
}

export default Result;