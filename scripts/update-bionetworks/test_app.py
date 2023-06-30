import pytest

from app import upgrade_schema_to_17_1_0, add_bionetwork, Project, HCABionetwork
from assertpy import assert_that


def test_upgrade_to_supported_version():
    source_version = '17.0.0'
    project = Project().with_schema_version(source_version)
    upgrade_schema_to_17_1_0(project, 'test_uuid')
    assert_that(project.content['describedBy']) \
        .contains('17.1.0') \
        .does_not_contain(source_version)


def test_upgrade_to_unsupported_version():
    source_version = '16.0.0'
    project = Project().with_schema_version(source_version)
    with pytest.raises(ValueError, match=f'need to upgrade schema .* version is {source_version}'):
        upgrade_schema_to_17_1_0(project, 'test_uuid')


def test_add_bionetwork():
    project = Project().with_schema_version('17.1.0')
    test_bionetwork = HCABionetwork(name='Blood',
                                    hca_tissue_atlas='Blood',
                                    hca_tissue_atlas_version='v1.0',
                                    atlas_project=False)
    add_bionetwork(project, test_bionetwork)
    assert_that(project.content).contains_key('hca_bionetworks')
    assert_that(project.content['hca_bionetworks']) \
        .is_length(1) \
        .contains(test_bionetwork)
    assert_that(project.content['hca_bionetworks'][0]).is_type_of(dict)


def test_add_bionetwork_idempotent():
    project = Project().with_schema_version('17.1.0')
    test_bionetwork = HCABionetwork(name='Blood',
                                    hca_tissue_atlas='Blood',
                                    hca_tissue_atlas_version='v1.0',
                                    atlas_project=False)
    add_bionetwork(project, test_bionetwork)
    add_bionetwork(project, test_bionetwork)
    assert_that(project.content['hca_bionetworks']) \
        .is_length(1) \
        .contains(test_bionetwork)


def test_add_2_networks():
    project = Project().with_schema_version('17.1.0')
    test_bionetwork2 = HCABionetwork(name='Kidney',
                                     hca_tissue_atlas='Kidney',
                                     hca_tissue_atlas_version='v1.0',
                                     atlas_project=False)
    test_bionetwork1 = HCABionetwork(name='Blood',
                                     hca_tissue_atlas='Blood',
                                     hca_tissue_atlas_version='v1.0',
                                     atlas_project=False)
    add_bionetwork(project, test_bionetwork1)
    add_bionetwork(project, test_bionetwork2)
    assert_that(project.content['hca_bionetworks']) \
        .is_length(2) \
        .contains(test_bionetwork1) \
        .contains(test_bionetwork2)


def test_update_network():
    project = Project().with_schema_version('17.1.0')
    orig_bionetwork = HCABionetwork(name='Blood',
                                    hca_tissue_atlas='Blood',
                                    hca_tissue_atlas_version='v1.0',
                                    atlas_project=False)
    another_bionetwork = HCABionetwork(name='Kidney',
                                    hca_tissue_atlas='Kidney',
                                    hca_tissue_atlas_version='v2.0',
                                    atlas_project=False)
    updated_bionetwork = HCABionetwork(name='Blood',
                                    hca_tissue_atlas='Blood',
                                    hca_tissue_atlas_version='v2.0',
                                    atlas_project=False)
    add_bionetwork(project, orig_bionetwork)
    add_bionetwork(project, another_bionetwork)
    add_bionetwork(project, updated_bionetwork)
    assert_that(project.content['hca_bionetworks']) \
        .is_length(2) \
        .contains(updated_bionetwork) \
        .contains(another_bionetwork) \
        .does_not_contain(orig_bionetwork)
