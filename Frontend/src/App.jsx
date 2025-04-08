import { useState } from 'react'
import './App.css'
import { SearchBar } from './SearchBar'
import { ChartSection } from './Chart'

function App() {

  return (
    <>
      <SearchBar />
      <div className='ChartSection'>
        <ChartSection />
      </div>
    </>
  )
}


export default App
