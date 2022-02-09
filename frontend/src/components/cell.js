import React, { useState } from 'react';
import { InputText } from 'primereact/inputtext';
import '../styles/Cell.css';


const Cell = ({ content }) => {

    const [value, setValue] = useState('');

    return (
        <span className="card">
            {content !== '#' ?
                <InputText className='cell border-noround' maxLength="1" id="username" value={value} onChange={(e) => setValue(e.target.value.toUpperCase())} keyfilter={/^[a-zöäüõ ]$/} placeholder={content} />
                : <div className='cell bg-black-alpha-90 border-noround'></div>
            }
        </span>
    )

}

export default Cell