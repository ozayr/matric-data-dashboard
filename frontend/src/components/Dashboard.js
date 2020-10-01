import React, { Component } from 'react'
import BarGraph from './BarGraph';
// import LineGraph from './LineGraph';



class Dashboard extends Component {
  constructor(props) {
    super(props);
 
    this.state = {
      parsed_data: {},
    };
  }

  componentDidMount() {
    fetch('http://ec2-13-245-11-188.af-south-1.compute.amazonaws.com:9000/get_charts/')
      .then(res => res.json())
      .then(res => this.setState({ parsed_data: JSON.parse(res) }));
  
  }
  
  render() {
    return (
      <div className="content">
        <div className="container-fluid">

          <div className="row">
            <div className="col-md-12">
              <BarGraph title = {"Number of Schools"}
              subtitle = {"by Province"} 
              data = {this.state.parsed_data.schools_in_province} 
              show_legend={false}/>
            </div>
          </div>

          <div className="row">
          <div className="col-md-12">
              <BarGraph title = {"Number of Candidates that wrote"}
              subtitle = {"by Province"} 
              data={this.state.parsed_data.wrote_2014_province} 
              show_legend={true}/>
            </div>
          </div>

          <div className="row">
          <div className="col-md-12">
              <BarGraph title = {"Pass Rate"}
              subtitle = {"by Province"} 
              data={this.state.parsed_data.passrate_2014_province} 
              show_legend={true}/>
            </div>
          </div>

        </div>
      </div>
    )
  }
}

export default Dashboard