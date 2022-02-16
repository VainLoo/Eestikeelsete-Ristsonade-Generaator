import './styles/App.css';
import Crossword from './components/crossword'
import React, { useState, useEffect } from 'react';
import { CrosswordService } from './CrosswordService';
import { Button } from 'primereact/button';
import Clues from './components/clues';
import { Card } from 'primereact/card';
import { InputNumber } from 'primereact/inputnumber';
import '/node_modules/primeflex/primeflex.css';

function App() {

  const [loading1, setLoading1] = useState(false);
  const [words, setWords] = useState({});
  const [grid, setGrid] = useState([]);
  const [check, setCheck] = useState(false);
  const [reset, setReset] = useState(false);
  const [sizeWidth, setWitdh] = useState(10);
  const [sizeLength, setLength] = useState(10);
  const [response, setResponse] = useState()
  const crosswordService = new CrosswordService(setResponse);

  useEffect(() => {
    if (response) {
      console.log(response);
      setWords(response.data.job_result.words);
      setLoading1(false);
      setGrid(response.data.job_result.grid);
    }
  }, [response])


  const getData = () => {
    setWords({});
    setGrid([]);
    setLoading1(true);
    setCheck(false);
    setReset(true);
    crosswordService.postCrossword(sizeLength, sizeWidth).then(res => {
      crosswordService.getStatus(res.data.job_id)
    });
  }


  return (
    <div>
      <Card title="Ristsõna">
        <div className="p-fluid grid formgrid">
          <div className="field col-2">
            <h3>Ristsõna suurus</h3>
            <label>Pikkus</label>
            <InputNumber className='mb-2' inputId="minmax-buttons" value={sizeLength} onValueChange={(e) => setLength(e.value)} showButtons mode="decimal" showButtons min={4} max={20}
              decrementButtonClassName="p-button-secondary noMargin" incrementButtonClassName="p-button-secondary noMargin" />
            <label>Laius</label>
            <InputNumber inputId="minmax-buttons" value={sizeWidth} onValueChange={(e) => setWitdh(e.value)} showButtons mode="decimal" showButtons min={4} max={20}
              decrementButtonClassName="p-button-secondary noMargin" incrementButtonClassName="p-button-secondary noMargin" />
          </div>
        </div>
        <div className="grid p-fluid">
          <div className='field col-2'>
            <Button label="Loo Ristsõna" loading={loading1} onClick={getData} />
            {grid.length > 0 ? <Button label="Kontrolli" onClick={() => setCheck(true)} />
              : <Button label="Kontrolli" onClick={() => setCheck(true)} disabled />
            }
          </div>
        </div>
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