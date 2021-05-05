import { Component } from "react";
import styles from '../styles/Result.module.css';

class Result extends Component {
  render() {
    if (this.props.type === "so") {
      console.log("SOOOO")
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
        console.log("GH")
        return (
            <div className={styles.container}>
                <div className={styles.questionContainer}>
                    <div className="bold">Question:&nbsp;</div>
                    <a href={this.props.url}>{this.props.title}</a>
                </div>
                <div className={styles.questionContainer}>
                    <div className="bold">Answer Star Score:&nbsp;</div>
                    <div>{this.props.starScore}</div>
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
    }
  }
}

export default Result;