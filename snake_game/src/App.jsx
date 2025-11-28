import React from 'react'
import SnakeGame from './SnakeGame'

export default function App() {
  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-2xl font-semibold text-center mb-3">Snake — React</h1>
      <SnakeGame />
      <footer className="footer">Use arrow keys or WASD to move. Space to pause.</footer>
    </div>
  )
}
