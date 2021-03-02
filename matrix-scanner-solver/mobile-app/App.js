import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

import CameraPage from './src/camera.page'
import styles from './src/styles';

export default function App() {
  return (
    <View style={styles.container}>
      <Text style={styles.headerText}>Welcome to Matrix Scanner Solver!</Text>
      <StatusBar style="auto"/>
      <CameraPage/>
    </View>   
  );
}

