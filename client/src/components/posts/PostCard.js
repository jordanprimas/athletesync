import React, { useState, useEffect } from 'react';
import { GoHeartFill, GoHeart } from "react-icons/go";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";

dayjs.extend(relativeTime);
dayjs.extend(utc);

const PostCard = ({ post, postLikes, handleAddLike, user, handleDeleteLike }) => {
  const [liked, setLiked] = useState(false);

  const like = postLikes.find(like => like.user_id === user.id)

  useEffect(() => {
    if (like) {
      setLiked(true)
    } else {
      setLiked(false)
    }
  }, [postLikes, user.id])

  

  const handleLikeClick = () => {
    if (!liked) {
      setLiked(true);
      fetch("/api/likes", {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_id: user.id,
          post_id: post.id,
        }),
      })
      .then(res => {
        if (res.ok) {
          return res.json()
        } else {
          throw new Error("Failed to like post")
        }
      })
      .then(data => handleAddLike(data))
      .catch(error => {
        console.error("Error liking post:", error)
        setLiked(false)
      });
    } else {
      setLiked(false)
      fetch(`/api/likes/${like.id}`, {
        method: "DELETE",
      })
      .then((res) => {
        if (res.ok) {
          return res.json()
        } else {
          throw new Error("Failed to unlike post")
        }
      })
      .then((deletedLike) => handleDeleteLike(deletedLike))
      .catch(error => {
        console.error("Error unliking post:", error)
        setLiked(true)
      })
    }
  };

  return (

    <div>
      {/* Post Card */}
      <div  
        key={post.id}
        className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm
        hover:shadow-md hover:-translate-y-1 transition-all duration-200 max-w-2xl w-full mx-auto"
      >
        {/* Card Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-[#86ABBD] text-white flex items-center justify-center font-semibold">
              {post.user.username[0].toUpperCase()}
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <p className="font-semibold text-gray-800">{post.user.username}</p>
              <span className="w-1 h-1 bg-gray-400 rounded-full inline-block"></span>
              <span>{dayjs.utc(post.created_at).local().fromNow()}</span>
            </div>
          </div>
        </div>

        {/* Card Content */}
        <div className="space-y-3 mb-4">
          <h3 className="text-lg font-semibold text-gray-900">{post.title}</h3>
          <p className="text-gray-700 leading-relaxed">{post.content}</p>
        </div>

        {/* Card Footer */}
        <div className="flex items-center text-sm gap-2">
          <button
            onClick={handleLikeClick}
            className="focus:outline-none"
          >
            {liked ? (
              < GoHeartFill className="text-[#FF7E6B] w-5 h-5" /> 
            ) : (
              < GoHeart className="text-gray-400 w-5 h-5 hover:text-[#FF7E6B]" />
            )}
          </button>
          <span>{postLikes.length}</span>
        </div>
      </div>
    </div>
  );
};

export default PostCard;
