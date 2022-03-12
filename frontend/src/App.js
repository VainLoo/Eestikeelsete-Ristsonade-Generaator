import './styles/App.css';
import '/node_modules/primeflex/primeflex.css';
import React, { useState, useEffect, useRef } from 'react';
import PrintComponent from './components/printComponent';
import { CrosswordService } from './CrosswordService';
import { Button } from 'primereact/button';
import { Card } from 'primereact/card';
import { Divider } from 'primereact/divider';
import { Toast } from 'primereact/toast';

import { useReactToPrint } from 'react-to-print';

function App() {

  const [loading1, setLoading1] = useState(false);
  const [words, setWords] = useState({});
  const [grid, setGrid] = useState([]);
  const [check, setCheck] = useState(false);
  const [checkIcon, setCheckIcon] = useState('pi pi-times');
  const [reset, setReset] = useState(false);
  //const [sizeWidth, setWitdh] = useState(10);
  //const [sizeLength, setLength] = useState(10);
  const [response, setResponse] = useState()
  const toast = useRef(null);
  const crosswordService = new CrosswordService(setResponse);

  const componentRef = useRef();
  const handlePrint = useReactToPrint({
    content: () => componentRef.current,
  });

  useEffect(() => {
    document.title = "Eestikeelsete Ristsõnade Generaator"
  }, [])

  useEffect(() => {
    if (response) {
      if (response === 'failed') {
        console.log("Failed to fetch crossword");
        showError();
        setLoading1(false);
      } else {
        //console.log(response);
        showSuccess();
        setWords(response.data.job_result.words);
        setLoading1(false);
        setGrid(response.data.job_result.grid);
      }

    }
  }, [response])

  const showError = () => {
    toast.current.show({ severity: 'error', summary: 'Viga genereerimisel', detail: '', life: 3000 });
  }

  const showSuccess = () => {
    toast.current.show({ severity: 'success', summary: 'Ristsõna edukalt genereeritud', detail: '', life: 3000 });
  }


  const getData = () => {
    setWords({});
    setGrid([]);
    setLoading1(true);
    setCheck(false);
    setReset(true);
    setCheckIcon('pi pi-times')
    crosswordService.postCrossword().then(res => {
      if (res.data.job_status === 'finished') {
        setResponse(res);
      } else {
        crosswordService.getStatus()
      }

    });
  }


  return (
    <div>
      <Toast ref={toast} />
      <Card title="Eestikeelsete ristsõnade generaator">
        <div className="grid p-fluid">
          <div className='field col-12 lg:col-3'>
            <Button label="Loo Ristsõna" icon="pi pi-star-fill" iconPos="right" loading={loading1} onClick={getData} />
            {grid.length > 0 ? <Button onClick={() => {setCheck(!check); check ? setCheckIcon('pi pi-times') : setCheckIcon('pi pi-check')}} icon={checkIcon} iconPos="right" label="Kontrolli"/>
              : <Button icon={checkIcon} iconPos="right" label="Kontrolli" disabled />
            }
            {grid.length > 0 ? <Button label="Prindi" icon="pi pi-print" iconPos="right" onClick={handlePrint} />
              : <Button icon="pi pi-print" iconPos="right" label="Prindi" disabled />
            }

          </div>
        </div>
      </Card>


      <PrintComponent ref={componentRef} check={check} grid={grid} reset={reset} words={words} setReset={setReset} />

      <footer>
        <Divider />
        <div className='flex align-content-end justify-content-center'>
          <p className='font-bold text-gray-700 relative bottom-0'>Copyright © 2022 Allan Loo</p>
        </div>
      </footer>
    </div>
  );
}

export default App;