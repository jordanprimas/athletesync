import React, { useContext, useState, useEffect } from "react";
import { Routes, Route } from 'react-router-dom';
import NavBar from "./components/pages/Navbar";
import PostList from "./components/posts/PostList";
import PostForm from "./components/posts/PostForm";
import Home from "./components/pages/Home";
import Authentication from "./components/pages/Authentication";
import DiscoverGroups from "./components/pages/DiscoverGroups";
import GroupDetail from "./components/groups/GroupDetail.js";
import { GroupContext } from "./contexts/GroupContext";
import { PostContext } from "./contexts/PostContext";
import { UserContext } from "./contexts/UserContext";
import './index.css';


const App = () => {
  const [user, setUser] = useContext(UserContext)
  const [posts, setPosts] = useContext(PostContext)
  const [groups, setGroups] = useContext(GroupContext)
  const [likes, setLikes] = useState([])

  
  useEffect(() => {
    fetch('/api/likes')
    .then(res => res.json())
    .then(data => setLikes(data))
  }, [])


  const updateUser = (user) => setUser(user)

  const addPost = (post) => {
    setPosts([...posts, post])
  }


  const updateGroup = (updatedUserGroup) => {
    const group = groups.find(group => group.id === updatedUserGroup.group.id)
    console.log(updatedUserGroup)
    const updatedUserGroups = [...group.user_groups, updatedUserGroup]
    console.log(updatedUserGroups)
    const updatedGroup = {
      ...group,
      user_groups: updatedUserGroups
    }
    console.log(updatedGroup)

    const updatedGroups = groups.map(group => {
      if (group.id === updatedGroup.id) {
        return updatedGroup
      } else {
        return group
      }
    })
    setGroups(updatedGroups)
  }

  const deleteUserGroup = (deletedUserGroup) => {
    const group = groups.find(group => group.id === deletedUserGroup.group.id) 
    const userGroupIndex = group.user_groups.findIndex(userGroup => userGroup.id === deletedUserGroup.id)
    const userGroups = group.user_groups
    const removedUserGroup = userGroups.splice(userGroupIndex, 1)
    console.log(userGroups)

    const updatedGroup = {
      ...group,
      user_groups: userGroups
    }
    console.log(updatedGroup)
    const updatedGroups = groups.map(group => {
      if (group.id === updatedGroup.id) {
        return updatedGroup
      } else {
        return group
      }
    })
    setGroups(updatedGroups)
  }
  


  const handleEditClick = (id, newPostObj) => {
    fetch(`/api/posts/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: newPostObj.title,
        content: newPostObj.content,
      }),
    })
    .then((res) => res.json())
    .then(updatedPost => {
      const updatedPosts = posts.map(post => {
        return post.id === id ? { ...post, ...updatedPost } : post
      })
      setPosts(updatedPosts)
    })
  }

  const handleDeleteClick = (id) => {
    fetch(`/api/posts/${id}`,{
      method: "DELETE",
    })
    .then((res) => res.json())
    .then((deletedPost) => onDeletePost(deletedPost))
  }

  const onDeletePost = (deletedPost) => {
    const filteredPosts = posts.filter(post => post.id !== deletedPost.id)
    setPosts(filteredPosts)
  }

  const handleAddLike = (newLike) => {
    setLikes([...likes, newLike])
  }

  const handleDeleteLike = (deletedLike) => {
    const filteredLikes = likes.filter(like => like.id !== deletedLike.id)
    setLikes(filteredLikes)
  }

  
  if(!user)return(
    <>
    <Authentication updateUser={updateUser}/>
    </>
  )
  
  return (
    // Render Navbar
    <Routes>
      <Route element={<NavBar updateUser={updateUser} />} >
        <Route path="/" element={<Home user={user} posts={posts} handleDeleteClick={handleDeleteClick} handleEditClick={handleEditClick} />} />
        <Route path="/posts" element={<PostList posts={posts} likes={likes} handleAddLike={handleAddLike} user={user} handleDeleteLike={handleDeleteLike} />} />
        <Route path="/posts/new" element={<PostForm addPost={addPost} />} />
        <Route path="/Authentication" element={<Authentication updateUser={updateUser} />} />
        <Route path="/groups" element={<DiscoverGroups groups={groups} user={user} />} />
        <Route path="/groups/:id" element={<GroupDetail updateGroup={updateGroup} deleteUserGroup={deleteUserGroup} />} />
      </Route>
    </Routes>
  );
}

export default App;
