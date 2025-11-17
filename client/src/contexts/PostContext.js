import React, { useState, useEffect } from 'react'

const PostContext = React.createContext()

const PostProvider = ({ children }) => {
    const [posts, setPosts] = useState([])

    useEffect(() => {
        fetchPosts()
      }, [])

    const fetchPosts = () => {
        fetch('/api/posts')
        .then(res => res.json())
        .then(data => setPosts(data))
      }

      return(
        <PostContext.Provider value={[posts, setPosts]}>{children}</PostContext.Provider>
      )
}

export {PostContext, PostProvider}