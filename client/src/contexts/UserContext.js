import React, { useState, useEffect } from 'react'

const UserContext = React.createContext()

const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        fetchUser()
      }, [])
    
      
    
      const fetchUser = () =>{
        fetch('/api/authorized')
        .then(res => {
          if(res.ok){
            res.json().then(user => setUser(user))
          }else{
            setUser(null)
          }
        })
      }

      return(
        <UserContext.Provider value={[user, setUser]}>{children}</UserContext.Provider>
      )
}

export {UserContext, UserProvider}