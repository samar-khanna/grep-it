import { Component } from "react";
import ReactDOM from 'react-dom';
import styles from '../styles/Result.module.css';

class Result extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div className={styles.container}>
                <div className={styles.answerContainer}>
                    <div
                        className={styles.answer}
                        dangerouslySetInnerHTML={{
                            __html: this.props.answer
                        }}
                    />
                </div>
                <div className={styles.urlContainer}>
                    <div className="bold">Link to post:&nbsp;</div>
                    <a href={this.props.url}>{this.props.title}</a>
                </div>
            </div>
        )
    }
}

export default Result;