# Milestone Submission Workflow

## Overview
The milestone completion workflow has been updated so that:
- **Freelancers** submit a link (proof of work) instead of directly marking milestones as complete
- **Only Clients** can mark milestones as complete after reviewing the submitted work

## Changes Made

### 1. Database Model (`models.py`)
- Added `SubmissionLink` column to `Milestone` model (VARCHAR 500)
- Updated `Status` field to support three states:
  - `pending` - Milestone created, awaiting freelancer submission
  - `submitted` - Freelancer has submitted work link, awaiting client approval
  - `completed` - Client has approved and marked as complete

### 2. Migration Script (`add_submission_link.py`)
- Run this script once to update existing databases:
  ```bash
  python add_submission_link.py
  ```

### 3. Routes (`app.py`)

#### New Route: `/milestones/<id>/submit` (POST)
- **Purpose**: Freelancer submits work link
- **Access**: Only assigned freelancer
- **Validation**: 
  - Checks sequential order (previous milestones must be completed)
  - Requires valid submission link
- **Action**: Updates milestone status to 'submitted'

#### Updated Route: `/milestones/<id>/complete` (POST)
- **Purpose**: Client approves and completes milestone
- **Access**: Only project client
- **Validation**: Milestone must be in 'submitted' status
- **Action**: Updates milestone status to 'completed'

### 4. Template Updates (`templates/projects/project_details.html`)

#### For Freelancers:
- Shows input field to submit link for pending milestones
- Displays submission link once submitted
- Sequential locking (must complete previous milestones first)

#### For Clients:
- Shows submitted link for review
- "Approve & Complete" button for submitted milestones
- Can view all submission links

#### Status Badges:
- **Pending** (gray) - Awaiting freelancer submission
- **Submitted** (blue) - Awaiting client approval
- **Completed** (green) - Approved by client

## Workflow Example

1. **Client creates milestones** for the project
2. **Freelancer submits work** by entering a link (GitHub, Google Drive, etc.)
   - Status changes to "Submitted"
3. **Client reviews** the submission link
4. **Client approves** by clicking "Approve & Complete"
   - Status changes to "Completed"
5. **Next milestone** becomes available for freelancer

## Benefits

- ✅ Clear separation of responsibilities
- ✅ Client has final approval authority
- ✅ Proof of work is preserved via submission links
- ✅ Sequential workflow ensures quality control
- ✅ Transparent progress tracking for both parties
