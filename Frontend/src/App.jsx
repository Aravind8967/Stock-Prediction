import { useState } from 'react'
import './App.css'
import { SearchBar } from './SearchBar'
import { ChartSection } from './Chart'
import { ChatLauncher } from './AIChat'

function App() {

  return (
    <>
      <ChatLauncher />
      <SearchBar />
      <div className='ChartSection'>
        <ChartSection />
      </div>
    </>
  )
}


export default App
