# server/seed.py

from random import choice, randint, sample
from datetime import datetime, timedelta
from faker import Faker

from server.app import app
from server.models import (
    db, User, AthleteProfile, Group, UserGroup, GroupPost,
    Comment, Like, Document, SOAPNote, Addendum, WellnessEntry
)

fake = Faker()

NUM_USERS = 10
NUM_GROUPS = 5
NUM_POSTS_PER_GROUP = 5
NUM_WELLNESS_ENTRIES_PER_ATHLETE = 5
NUM_DOCS_PER_ATHLETE = 3
NUM_SOAP_NOTES_PER_ATHLETE = 3
NUM_COMMENTS = 50
NUM_LIKES = 100
NUM_ADDENDUMS = 30

with app.app_context():
    print("🌱 Seeding database...")

    # Clear existing data
    db.session.query(Addendum).delete()
    db.session.query(Comment).delete()
    db.session.query(Like).delete()
    db.session.query(Document).delete()
    db.session.query(SOAPNote).delete()
    db.session.query(WellnessEntry).delete()
    db.session.query(GroupPost).delete()
    db.session.query(UserGroup).delete()
    db.session.query(Group).delete()
    db.session.query(AthleteProfile).delete()
    db.session.query(User).delete()
    db.session.commit()

    # ------------------ Users ------------------
    users = []
    for _ in range(NUM_USERS):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
        )
        user.password_hash = "password123"
        db.session.add(user)
        users.append(user)
    db.session.flush()  # flush to get ids

    # ------------------ Athlete Profiles ------------------
    athlete_profiles = []
    for user in users:
        profile = AthleteProfile(
            user_id=user.id,
            sport=fake.word(),
            position=fake.word(),
            height=randint(60, 78),  # inches
            weight=randint(120, 220),
            dob=fake.date_of_birth(minimum_age=18, maximum_age=35),
            injury_history=fake.sentence()
        )
        db.session.add(profile)
        athlete_profiles.append(profile)

    # ------------------ Groups ------------------
    groups = []
    for _ in range(NUM_GROUPS):
        group = Group(
            name=fake.word(),
            description=fake.sentence(),
            cover_image=fake.image_url()
        )
        db.session.add(group)
        groups.append(group)
    db.session.flush()

    # ------------------ UserGroups ------------------
    for group in groups:
        for user in sample(users, k=randint(2, len(users))):
            user_group = UserGroup(user_id=user.id, group_id=group.id)
            db.session.add(user_group)

    # ------------------ Group Posts ------------------
    posts = []
    for group in groups:
        for _ in range(NUM_POSTS_PER_GROUP):
            author = choice(users)
            post = GroupPost(
                group_id=group.id,
                author_id=author.id,
                content=fake.sentence()
            )
            db.session.add(post)
            posts.append(post)

    # ------------------ Wellness Entries ------------------
    wellness_entries = []
    for profile in athlete_profiles:
        for _ in range(NUM_WELLNESS_ENTRIES_PER_ATHLETE):
            entry = WellnessEntry(
                athlete_id=profile.user_id,
                sleep_quality=randint(4, 10),
                mood=randint(4, 10),
                fatigue=randint(1, 10),
                soreness=randint(1, 10),
                stress=randint(4, 10),
                notes=fake.sentence(),
                created_at=fake.date_time_this_year()
            )
            db.session.add(entry)
            wellness_entries.append(entry)

    # ------------------ Documents ------------------
    documents = []
    for profile in athlete_profiles:
        for _ in range(NUM_DOCS_PER_ATHLETE):
            doc = Document(
                athlete_id=profile.user_id,
                trainer_id=choice(users).id,
                title=fake.sentence(),
                description=fake.text(),
                category=fake.word(),
                file_url=fake.url(),
                created_at=fake.date_time_this_year()
            )
            db.session.add(doc)
            documents.append(doc)

    # ------------------ SOAP Notes ------------------
    soap_notes = []
    for profile in athlete_profiles:
        for _ in range(NUM_SOAP_NOTES_PER_ATHLETE):
            note = SOAPNote(
                athlete_id=profile.user_id,
                trainer_id=choice(users).id,
                subjective=fake.sentence(),
                objective=fake.sentence(),
                assessment=fake.sentence(),
                plan=fake.sentence(),
                injury_location=fake.word(),
                injury_type=fake.word(),
                created_at=fake.date_time_this_year()
            )
            db.session.add(note)
            soap_notes.append(note)

    db.session.flush()

    # ------------------ Comments ------------------
    all_targets = []
    for p in posts:
        all_targets.append((p, "post"))
    for w in wellness_entries:
        all_targets.append((w, "wellness_entry"))
    for s in soap_notes:
        all_targets.append((s, "soap_note"))
    for d in documents:
        all_targets.append((d, "document"))

    for _ in range(NUM_COMMENTS):
        target_obj, target_type = choice(all_targets)
        comment = Comment(
            author_id=choice(users).id,
            target_type=target_type,
            target_id=target_obj.id,
            message=fake.sentence()
        )
        db.session.add(comment)

    # ------------------ Likes ------------------
    for _ in range(NUM_LIKES):
        target_obj, target_type = choice(all_targets[:])  # reuse same targets
        like = Like(
            user_id=choice(users).id,
            target_type=target_type,
            target_id=target_obj.id,
            like_type=choice(["like", "verify"])
        )
        db.session.add(like)

    # ------------------ Addendums ------------------
    for _ in range(NUM_ADDENDUMS):
        target_obj, target_type = choice(all_targets[:])
        addendum = Addendum(
            author_id=choice(users).id,
            target_type=target_type,
            target_id=target_obj.id,
            content=fake.sentence(),
            annotation_type="revision",
            created_at=fake.date_time_this_year()
        )
        db.session.add(addendum)

    # Commit everything
    db.session.commit()
    print("✅ Database seeding complete!")
