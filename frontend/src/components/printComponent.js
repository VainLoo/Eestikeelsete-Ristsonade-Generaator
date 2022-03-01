import Clues from './clues';
import Crossword from './crossword'
import React from 'react';

const PrintComponent = React.forwardRef(({ check, grid, reset, words, setReset }, ref) => {
    return (
        <div ref={ref} className='grid flex justify-content-center flex-wrap'>
            <div className='col flex align-items-start justify-content-center p-3'>
                <Crossword check={check} grid={grid} reset={reset} setReset={setReset}></Crossword>
            </div>
            <div className='col p-4'>
                <Clues words={words} check={check}></Clues>
            </div>
        </div>
    )
});



export default PrintComponent