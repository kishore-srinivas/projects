import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { Button, StyleSheet, Text, View } from 'react-native';

import CameraPage from './src/camera.page'
import styles from './src/styles';

class MainView extends React.Component {
  state = {
    cameraOn: false,
    cameraButton: "Show Camera",
    text: {},
    isLoading: true,
  }

  toggleCamera() {
    this.setState({cameraOn: !this.state.cameraOn});
    this.setState({cameraButton: this.state.cameraOn ? "Show Camera" : "Hide Camera"});
  }

  // getOnlineData() {
  //   fetch('https://reactnative.dev/movies.json')
  //     .then((response) => response.json())
  //     .then((json) => {
  //       this.setState({text: json.movies });
  //     })
  //     .catch((error) => console.error(error))
  //     .finally(() => {
  //       this.setState({isLoading: false });
  //     });    
  // }

  render() {
    const {cameraOn, cameraButton, text, isLoading} = this.state;

    // let camera = <Text>{JSON.stringify(text[0])}</Text>;
    let camera = <Text>Camera is off</Text>
    if (cameraOn) camera = <CameraPage/>

    return (
      <View style={styles.container}>
        <Text style={styles.headerText}>Welcome to Matrix Scanner Solver!</Text>
        <StatusBar style="auto"/>

        <Button 
          // onPress={() => this.getOnlineData()}
          onPress={() => this.toggleCamera()}
          title={cameraButton}>
        </Button>

        {camera}
      </View>    
    );
  };
}

export default function App() {
  return (
    <MainView/>
  );
}

