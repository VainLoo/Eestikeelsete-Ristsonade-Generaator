import React, { useState, useEffect } from 'react';
import { InputText } from 'primereact/inputtext';
import '../styles/Cell.css';


const Cell = ({ cell, check, reset, setReset }) => {

    const [value, setValue] = useState('');
    const [truevalue] = useState(cell.contents);

    useEffect(() => {
        if (reset) setValue('');
        setReset(false);
    }, [reset]);

    return (
        <div>
            {cell.contents !== '#' ?
                <div className='box'>
                    <i className="cornerNumber p-component">{cell.clueNumber}</i>
                    {check ? value === truevalue ? truevalue === " " ? <InputText disabled className='cell border-noround' maxLength="1" id="cell" value={cell.contents} data-truevalue={truevalue} tooltip="See on tühik" tooltipOptions={{ showOnDisabled: true }}/> 
                        : <InputText className='cell rightCell border-noround' maxLength="1" id="cell" value={value} onChange={(e) => setValue(e.target.value.toUpperCase())} keyfilter={/^[a-zöäüõšžA-ZÖAÖÜŠŽ ]$/} data-truevalue={truevalue} />
                        : truevalue === " " ? <InputText disabled className='cell border-noround' maxLength="1" id="cell" value={cell.contents} data-truevalue={truevalue} tooltip="See on tühik" tooltipOptions={{ showOnDisabled: true }}/> 
                        : <InputText className='cell wrongCell border-noround' maxLength="1" id="cell" value={value} onChange={(e) => setValue(e.target.value.toUpperCase())} keyfilter={/^[a-zöäüõšžA-ZÖAÖÜŠŽ ]$/} data-truevalue={truevalue} />
                        : truevalue === " " ? <InputText disabled className='cell border-noround' maxLength="1" id="cell" value={cell.contents} data-truevalue={truevalue} tooltip="See on tühik" tooltipOptions={{ showOnDisabled: true }}/> 
                        : <InputText className='cell border-noround' maxLength="1" id="cell" value={value} onChange={(e) => setValue(e.target.value.toUpperCase())} keyfilter={/^[a-zöäüõšžA-ZÖAÖÜŠŽ ]$/} data-truevalue={truevalue} />
                    }

                </div>
                : <div className='cell bg-black-alpha-90 border-noround'></div>
            }
        </div>
    )

}

export default Cell