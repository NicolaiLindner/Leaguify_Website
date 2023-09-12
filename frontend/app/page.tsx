"use client"
import React from 'react';
import MyButton from '../components/MyButton';
import GameDurationChart from '../components/GameDurationChart'

export default function Home() {
  return (
    <div>
      <MyButton />
        <GameDurationChart />
    </div>
  );
}
