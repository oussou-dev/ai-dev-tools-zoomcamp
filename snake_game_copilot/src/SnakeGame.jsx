import React, { useEffect, useRef, useState } from 'react'

const CANVAS_SIZE = 400
const SCALE = 20
const ROWS = CANVAS_SIZE / SCALE

function randomPosition() {
  return {
    x: Math.floor(Math.random() * ROWS),
    y: Math.floor(Math.random() * ROWS),
  }
}

export default function SnakeGame() {
  const canvasRef = useRef(null)
  const [snake, setSnake] = useState([{ x: Math.floor(ROWS / 2), y: Math.floor(ROWS / 2) }])
  const [dir, setDir] = useState({ x: 0, y: -1 })
  const [food, setFood] = useState(randomPosition)
  const [running, setRunning] = useState(false)
  const [gameOver, setGameOver] = useState(false)
  const [score, setScore] = useState(0)
  const speedRef = useRef(150)

  useEffect(() => {
    const handleKey = (e) => {
      const key = e.key
      setDir((prev) => {
        const isOpposite = (nx, ny) => nx === -prev.x && ny === -prev.y
        if (key === 'ArrowUp' || key === 'w' || key === 'W') return isOpposite(0, -1) ? prev : { x: 0, y: -1 }
        if (key === 'ArrowDown' || key === 's' || key === 'S') return isOpposite(0, 1) ? prev : { x: 0, y: 1 }
        if (key === 'ArrowLeft' || key === 'a' || key === 'A') return isOpposite(-1, 0) ? prev : { x: -1, y: 0 }
        if (key === 'ArrowRight' || key === 'd' || key === 'D') return isOpposite(1, 0) ? prev : { x: 1, y: 0 }
        if (key === ' ') {
          setRunning(r => !r)
          return prev
        }
        return prev
      })
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [])

  useEffect(() => {
    let id
    if (running && !gameOver) {
      id = setInterval(() => step(), speedRef.current)
    }
    return () => clearInterval(id)
  }, [running, dir, snake, food, gameOver])

  useEffect(() => draw(), [snake, food])

  function reset() {
    setSnake([{ x: Math.floor(ROWS / 2), y: Math.floor(ROWS / 2) }])
    setDir({ x: 0, y: -1 })
    setFood(randomPosition())
    setRunning(false)
    setGameOver(false)
    setScore(0)
    speedRef.current = 150
  }

  function step() {
    setSnake(prev => {
      const head = { x: prev[0].x + dir.x, y: prev[0].y + dir.y }
      // wall collision
      if (head.x < 0 || head.y < 0 || head.x >= ROWS || head.y >= ROWS) {
        setGameOver(true)
        setRunning(false)
        return prev
      }
      // self collision
      for (let cell of prev) if (cell.x === head.x && cell.y === head.y) {
        setGameOver(true)
        setRunning(false)
        return prev
      }

      const newSnake = [head, ...prev]
      // eat food
      if (head.x === food.x && head.y === food.y) {
        setFood(() => {
          let pos = randomPosition()
          while (newSnake.some(c => c.x === pos.x && c.y === pos.y)) pos = randomPosition()
          return pos
        })
        setScore(s => s + 1)
        // speed up slightly
        speedRef.current = Math.max(50, speedRef.current - 4)
        return newSnake
      }

      newSnake.pop()
      return newSnake
    })
  }

  function draw() {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    ctx.fillStyle = '#0b2a2a'
    ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE)

    // draw food
    ctx.fillStyle = '#e63946'
    ctx.fillRect(food.x * SCALE, food.y * SCALE, SCALE, SCALE)

    // draw snake
    ctx.fillStyle = '#8bd3c7'
    snake.forEach((cell, i) => {
      ctx.fillStyle = i === 0 ? '#56c596' : '#8bd3c7'
      ctx.fillRect(cell.x * SCALE, cell.y * SCALE, SCALE - 1, SCALE - 1)
    })
  }

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="flex gap-2 items-center">
        <button className="controls-btn" onClick={() => { if (!running && !gameOver) setRunning(true); if (gameOver) reset(); }}>
          {gameOver ? 'Restart' : running ? 'Running' : 'Start'}
        </button>
        <button className="controls-btn" onClick={() => setRunning(r => !r)}>{running ? 'Pause' : 'Resume'}</button>
        <div className="text-gray-300">Score: {score}</div>
      </div>
      <canvas ref={canvasRef} width={CANVAS_SIZE} height={CANVAS_SIZE} className="canvas" />
      {gameOver && <div className="overlay">Game Over — Score: {score}</div>}
    </div>
  )
}
