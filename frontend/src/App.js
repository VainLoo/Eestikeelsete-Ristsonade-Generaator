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
  const crosswordService = new CrosswordService();

  const getData = () => {
    setLoading1(true);
    crosswordService.getCrossword().then(data => { setWords(data.words); setLoading1(false); setGrid(data.grid) });
  }

  return (
    <div>
      <Card title="Ristsõna">
      <Button className='' label="Loo Ristsõna" loading={loading1} onClick={getData} />
      </Card>
      

      <div className='grid flex justify-content-center flex-wrap'>
        <div className='col-6 flex align-items-start justify-content-center'>
          <Crossword grid={grid}></Crossword>
        </div>
        <div className='col'>
          <Clues words={words}></Clues>
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