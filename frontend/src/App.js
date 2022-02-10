import './styles/App.css';
import Crossword from './components/crossword'
import React, { useState } from 'react';
//import { DataTable } from 'primereact/datatable';
//import { Column } from 'primereact/column';
import { CrosswordService } from './CrosswordService';
import { Button } from 'primereact/button';
import Clues from './components/clues';
import { Card } from 'primereact/card';
import '/node_modules/primeflex/primeflex.css';

function App() {

  const [loading1, setLoading1] = useState(false);
  const [words, setWords] = useState({});
  const [grid, setGrid] = useState([]);
  const [check, setCheck] = useState(false);
  const [reset, setReset] = useState(false);
  const crosswordService = new CrosswordService();


  const getData = () => {
    setWords({});
    setGrid([]);
    setLoading1(true);
    setCheck(false);
    setReset(true);
    crosswordService.getCrossword().then(data => { setWords(data.words); setLoading1(false); setGrid(data.grid);});
  }

  return (
    <div>
      <Card title="Ristsõna">
      <Button label="Loo Ristsõna" loading={loading1} onClick={getData} />
      {grid.length > 0 ? <Button label="Kontrolli" onClick={() => setCheck(true)} />
      : <Button label="Kontrolli" onClick={() => setCheck(true)} disabled />
      }
      </Card>
      

      <div className='grid flex justify-content-center flex-wrap'>
        <div className='col flex align-items-start justify-content-center'>
          <Crossword check={check} grid={grid} reset={reset} setReset={setReset}></Crossword>
        </div>
        <div className='col'>
          <Clues words={words} check={check}></Clues>
        </div>
      </div>

    </div>
  );
}

export default App;
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