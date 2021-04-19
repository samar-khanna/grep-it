import { Component } from "react";
import styles from '../styles/Result.module.css';

class Result extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        console.log(this.props)
        return (
            <div className={styles.resultBox}>
                <a href={this.props.url}> {this.props.title} </a>
            </div>
        )
    }
}

export default Result;