import { Component } from "react";
import styles from '../styles/Result.module.css';

class Result extends Component {
    // constructor(props) {
    //     super(props)

    //     this.state = {
    //         loaded: false
    //     };
    // }

    render() {
        if (this.props.type === "so") {
            return (
                <div className={styles.container}>
                    <div className={styles.questionContainer}>
                        <div className="bold">Question:&nbsp;</div>
                        <a href={this.props.url}>{this.props.title}</a>
                    </div>
                    <div className={styles.questionContainer}>
                        <div className="bold">Answer Upvote Score:&nbsp;</div>
                        <div>{this.props.upvoteScore}</div>
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
            // let answer = "Loading...";
            // fetch(`https://api.github.com/repos/${this.props.repo_name}/git/blobs/${this.props.blob_id}`, {
            //     method: "GET",
            //     headers: {
            //         "Accept": "application/vnd.github.v3+json",
            //         "Authorization": `Basic ${btoa("LucaKoval")}`
            //     },
            // })
            // .then(res => res.json())
            // .then(
            //     res => {
            //         answer = `<pre><code>${atob(res.content)}</code></pre>`
            //     },
            //     err => {
            //         console.log(`Error: ${err}`)
            //     }
            // )
            // if (!this.state.loaded) {
            console.log(this.props.answer.slice(0, 40))
                return (
                    <div className={styles.container}>
                        <div className={styles.questionContainer}>
                            <div className="bold">Repository:&nbsp;</div>
                            <a href={this.props.repo_link}>{this.props.repo_name}</a>
                        </div>
                        <div className={styles.questionContainer}>
                            <div className="bold">File:&nbsp;</div>
                            {this.props.filepath}
                        </div>
                        <div className={styles.questionContainer}>
                            <div className="bold">Answer Star Score:&nbsp;</div>
                            <div>{this.props.stars}</div>
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
            // }
        }
    }
}

export default Result;