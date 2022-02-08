import './App.css';
import Crossword from './components/crossword'
import React, { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { CrosswordService } from './CrosswordService';
import { Button } from 'primereact/button';
import Clues from './components/clues';
import { Card } from 'primereact/card';

function App() {

  const [loading1, setLoading1] = useState(false);
  const [words, setWords] = useState({});
  const [grid, setGrid] = useState([]);
  const crosswordService = new CrosswordService();
  /*
    useEffect(() => {
      crosswordService.getCrossword().then(data => {setWords(data.words); setLoading1(false); setGrid(data.grid)});
    }, []);
  */
  const getData = () => {
    setLoading1(true);
    crosswordService.getCrossword().then(data => { setWords(data.words); setLoading1(false); setGrid(data.grid) });
  }

  return (
    <div>
      <Card title="Ristsõna">
        <Button label="Loo Ristsõna" loading={loading1} onClick={getData} />
        {/*
        <div className="card">
            <DataTable value={words.across} responsiveLayout="scroll">
                <Column field="index" header="Index"></Column>
                <Column field="word" header="Word"></Column>
                <Column field="clue" header="Clue"></Column>
                <Column field="dir" header="Direction"></Column>
            </DataTable>
        </div>
        */}
        <Crossword grid={grid}></Crossword>
        <Clues words={words}></Clues>
      </Card>
    </div>
  );
}

export default App;
