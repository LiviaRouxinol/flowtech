import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

import LoginScreen from './screens/LoginScreen';
import HomeScreen from './screens/HomeScreen';
import ProductsScreen from './screens/ProductsScreen';
import HistoryScreen from './screens/HistoryScreen';
import SettingsScreen from './screens/SettingsScreen';
import MovimentacaoScreen from './screens/MovimentacaoScreen';
import EntryScreen from './screens/EntryScreen';
import ExitScreen from './screens/ExitScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarShowLabel: false,
        tabBarStyle: {
          backgroundColor: '#0F172A',
          borderTopWidth: 0,
          height: 65,
        },
        tabBarIcon: ({ focused, color }) => {
          let iconName;
          if (route.name === 'Home') iconName = focused ? 'home' : 'home-outline';
          else if (route.name === 'Produtos') iconName = focused ? 'cube' : 'cube-outline';
          else if (route.name === 'Movimentacao') iconName = focused ? 'swap-horizontal' : 'swap-horizontal-outline';
          else if (route.name === 'Histórico') iconName = focused ? 'time' : 'time-outline';
          else if (route.name === 'Ajustes') iconName = focused ? 'settings' : 'settings-outline';
          else if (route.name === 'Entrada') iconName = focused ? 'arrow-down-circle' : 'arrow-down-circle-outline';
          else if (route.name === 'Saída') iconName = focused ? 'arrow-up-circle' : 'arrow-up-circle-outline';
          else if (route.name === 'Entrada') iconName = focused ? 'arrow-down-circle' : 'arrow-down-circle-outline';
          else if (route.name === 'Saída') iconName = focused ? 'arrow-up-circle' : 'arrow-up-circle-outline';


          return <Ionicons name={iconName} size={24} color={focused ? '#3B82F6' : '#94A3B8'} />;
        },
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Produtos" component={ProductsScreen} />
      <Tab.Screen name="Movimentacao" component={MovimentacaoScreen} />
      <Tab.Screen name="Entrada" component={EntryScreen} />
      <Tab.Screen name="Saída" component={ExitScreen} />
      <Tab.Screen name="Histórico" component={HistoryScreen} />
      <Tab.Screen name="Ajustes" component={SettingsScreen} />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="App" component={TabNavigator} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
