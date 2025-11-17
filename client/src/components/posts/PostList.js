import React from "react";
import PostCard from "./PostCard"

const PostList = ({ posts, likes, handleAddLike, user, handleDeleteLike }) => {

  const postElementList = posts.map((post) => {
    const postLikes = likes.filter(like => like.post_id === post.id)
    return(
      <div className="">
        <PostCard key={post.id} post={post} postLikes={postLikes} handleAddLike={handleAddLike} user={user} handleDeleteLike={handleDeleteLike} />
      </div>
      
    )
})

  return (
    <div className="min-h-screen bg-[##F8FAFC] py-10 px-4">
      {/* Page Header */}
      <div className="max-w-6xl mx-auto mb-8 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Explore Posts</h1>
        <p className="text-sm text-gray-500">Discover what everyone's sharing 💬</p>
      </div>
      
      {/* Posts Grid */}
      <div className="max-w-6xl mx-auto grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {posts.length > 0 ? (
          postElementList
        ) : (
          <p className="text-gray-500 col-span-full text-center py-10">
            No posts yet - be the first to share something!
          </p>
        )}
        
      </div>
    
    </div>
    
  )
}

export default PostList;
