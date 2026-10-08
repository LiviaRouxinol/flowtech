import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

export default function App() {


  return (
    <View style={styles.container}>
      <Text style={styles.titulo}>Contador Inteligente</Text>

      <View style={styles.card}>
        <Text style={styles.contador}>{contador}</Text>
      </View>

      <TouchableOpacity
        style={styles.botao}
        onPress={() => setContador(contador + 1)}
      >
        <Text style={styles.textoBotao}>Aumentar</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.botaoReset}
        onPress={() => setContador(0)}
      >
        <Text style={styles.textoBotao}>Resetar</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20
  },

  titulo: {
    fontSize: 26,
    color: '#38bdf8',
    fontWeight: 'bold',
    marginBottom: 30
  },

  card: {
    backgroundColor: '#1e293b',
    padding: 30,
    borderRadius: 15,
    marginBottom: 30,
    elevation: 5
  },

  contador: {
    fontSize: 48,
    color: '#fff',
    fontWeight: 'bold'
  },

  botao: {
    backgroundColor: '#22c55e',
    paddingVertical: 12,
    paddingHorizontal: 40,
    borderRadius: 10,
    marginBottom: 15
  },

  botaoReset: {
    backgroundColor: '#ef4444',
    paddingVertical: 12,
    paddingHorizontal: 40,
    borderRadius: 10
  },

  textoBotao: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold'
  }
});