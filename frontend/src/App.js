import React, { Component } from "react";
import axios from "axios";

class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            jeuxList: [],
        }
    }

    componentDidMount() {
        this.refreshList();
    }

    refreshList(){
        axios
            .get('/api/jeux/')
            .then((res) => this.setState({jeuxList: res.data}))
            .catch((err) => console.log(err))
    }

    renderItems(){
        console.log(this.state)
        return this.state.jeuxList.map((jeu) => (
                <li key={jeu.id}>
                    {jeu.nom}
                </li>
            ))
    }

    render(){
        return (
            <div className="App">
                <ul className="">
                    {this.renderItems()}
                </ul>
            </div>
        )
    }
}

export default App;