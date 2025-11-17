from random import choice, randint
from faker import Faker
from app import app
from models import db, User, Post, Group, UserGroup, Like

fake = Faker()

if __name__ == "__main__":
    with app.app_context():
        print("🌱 Seeding database...")

        # Clear existing data
        db.session.query(Like).delete()
        db.session.query(Post).delete()
        db.session.query(UserGroup).delete()
        db.session.query(Group).delete()
        db.session.query(User).delete()
        db.session.commit()

        # --- USERS ---
        users = []
        for i in range(20):
            user = User(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password_hash="password123"  # Replace later with hash if using bcrypt
            )
            users.append(user)
        db.session.add_all(users)
        db.session.commit()
        print(f"✅ Created {len(users)} users")

        # --- GROUPS ---
        groups = []
        for i in range(100):
            group = Group(
                name=f"{fake.unique.word().capitalize()} {fake.word().capitalize()} Club",
                description=fake.paragraph(nb_sentences=3),
                cover_image=f"https://picsum.photos/seed/group{i}/600/400"
            )
            groups.append(group)
        db.session.add_all(groups)
        db.session.commit()
        print(f"✅ Created {len(groups)} groups")

        # --- POSTS ---
        posts = []
        for i in range(50):
            post = Post(
                title=" ".join(fake.words(nb=2)).title(),
                content=fake.paragraph(nb_sentences=4),
                image=f"https://picsum.photos/seed/post{i}/600/400",
                user_id=choice(users).id
            )
            posts.append(post)
        db.session.add_all(posts)
        db.session.commit()
        print(f"✅ Created {len(posts)} posts")

        # --- USER-GROUP RELATIONSHIPS ---
        user_groups = []
        for _ in range(60):
            ug = UserGroup(
                user_id=choice(users).id,
                group_id=choice(groups).id
            )
            user_groups.append(ug)
        db.session.add_all(user_groups)
        db.session.commit()
        print(f"✅ Created {len(user_groups)} user-group relationships")

        # --- LIKES ---
        likes = []
        for _ in range(150):
            like = Like(
                user_id=choice(users).id,
                post_id=choice(posts).id
            )
            likes.append(like)
        db.session.add_all(likes)
        db.session.commit()
        print(f"✅ Created {len(likes)} likes")

        print("Seeding complete!")