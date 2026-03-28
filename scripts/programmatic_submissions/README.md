# Programmatic submissions

## Purpose of this document

This document is intended to give an introduction to the HCA ingest service, specifically targeting data and metadata in the system and how they interact in the ingest ecosystem of data.

This document will be coupled with a set of python notebooks, which will show examples of how to interact with the data.

## Terminology
- HCA: Human Cell Atlas
- DCP: Data Coordination Platform
- Project: In the context of the HCA DCP Ingest Platform, the term `project` may have one of 2 meanings:
  1. When referring to metadata, the JSON file that contains the metadata about a project
  2. When referring to a submission/dataset, these 3 terms can be used interchangeably. Used to describe the 

## Understanding the metadata schema

The metadata schema is the staple of how data is interpreted in the system; it defines the content, validation rules and
structure of all the metadata that is in the system. For the Human Cell Atlas Data Coordination Platform, a JSON schema
was chosen to define the metadata in the system. For full details, please refer to the [metadata schema SLO](https://github.com/HumanCellAtlas/metadata-schema/blob/master/docs/metadata_slo.md)
and [rationale](https://github.com/HumanCellAtlas/metadata-schema/blob/master/docs/rationale.md) documents.

### Structure

The metadata schema is structured as stated in the [metadata entity model](https://github.com/HumanCellAtlas/metadata-schema/blob/master/docs/structure.md#metadata-entity-model)
of the [structure.md](https://github.com/HumanCellAtlas/metadata-schema/blob/master/docs/structure.md) document of the 
metadata schema repository.

For the purpose of this guide, "type entity" will be used to refer to the subtypes of the 5 major entities in the metadata model:
- Project: Contains information about the project, such as manuscript metadata, grants involved, contributors of the project etc
- File: Contains information about the data files, such as filename, description of the content, etc
- Biomaterial: Contains information about each of the biological materials used in the project, such as cell suspensions, specimens, etc.
- Project: Contains information about each of the protocols used on each step of the experiment.
- Process: Contains information about a process; usually, we don't need to worry a lot about processes, as they are used as intermediates in the system to create the relationships in between the other elements.

The schemas accepted for each of the major entities can be found always under the url `https://github.com/HumanCellAtlas/metadata-schema/tree/master/json_schema/type/{major_entity}`,
substituting `{type}` with  any of the major types described previously (e.g. https://github.com/HumanCellAtlas/metadata-schema/tree/master/json_schema/type/biomaterial)



### 

### What constitutes a project/submission

All our projects are made of "type entities", each one of those containing metadata that describes either a piece of experimental design.
These

Below you can find an example of a whole project and submission, and how the entities relate to each other: you can click on each of the 
entities to be redirected to the folder of the metadata schema that contains all the type entities of that class.

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2022-09-07T15:30:50.530Z\&quot; agent=\&quot;5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36\&quot; etag=\&quot;cRX-88NFg0As2ERGT6PV\&quot; version=\&quot;20.2.3\&quot; type=\&quot;google\&quot;&gt;&lt;diagram id=\&quot;Vtwi83Y6I7b7ka8JpLpU\&quot; name=\&quot;Page-1\&quot;&gt;7Vtbc5s6EP41fmwGxNWPuefhtEknc6btU0eAbJQA8gg5tvvrj8TNIGSMfXAcO00eglY3tN/ut1qJjIzreHlP4Sz8SgIUjYAWLEfGzQgA3XQA/yMkq1xiunYumFIcFI3Wgmf8BxVCrZDOcYDSRkNGSMTwrCn0SZIgnzVkkFKyaDabkKg56wxOUUvw7MOoLf2BAxbmUhc4a/kDwtOwnFm3x3lNDMvGxUrSEAZkURMZtyPjmhLC8qd4eY0iobxSL3m/uw211YtRlDBFh39TRB+9F6EToEXQ47hkjfJuEU5e83LImFDlpegI7qaYhXPvwicxLzzMY5iIaS9ZBFMuiBGDAWTwS+qHKIZcwihCogKmDFH+8JKS5Pe6djUTtTNK8vcAtff/MbG8X7cv9+b9w3f69idaTLD5xaj0Uq03ZasSC0rmSYBEf21kXC1CzNDzDPqidsGtj8tCFotl6vxxgqPomkSEZn2NyWQCfJ/LU0bJK6rVBLZnWzavyd/vDVGGlht1rNfe8B4RrhG64k2KDm6BdWnsRXGxthynNIewZjWmVghhYa3TauQ1oELNuVLKYg1itY0odWwW64TRvNDrUx2fmr65HlhTqU3lJSRBkqYLEYzwNOFFn+uN24VxJbSKuVddFhUxDgIxjRLFJs4DwGLqW3GxFbAYu6PSDwK7BUFL95wtZuIxIP48zpa5zeC9XGv/eJs8wBK/Qk4SVpPnPyrPsLOfYSAYNxHQNYVraAoMqkAwOAhOC4TnuRfjNMUkuU3eUEQEeZ2rSxgSVel6GxBdxVV7OMWmUHSFCY+SiGIYHSEqefLsndbidkYmLuAbEgFe6bd+RObBzlEqsJAbmCpfdIFnDOWLlfOV2Ns9sXcHCVObzIGHIR+l6XE2KOuZO81g3NMMdoMd6Rx4RwX72HYMOBDswJJgd/uFQfMdNye6vj00oiS4FDv7zMsg52u/qdwmV6IlZj/F84XrWEX5V1YuSzfLWtObVa3wxNmBL1XQdS5L+LJ/1gu1kURxPVRWKsfKl4CCVqohQceXSebURz15qAZxDUJLAWEpoyiCDL81X0OFazHDE8EJqwUNKYq3CCF//aJXPXmRBpJNEcgbYAbpFLHWQJmZVcveP/broGVm3zjFfD3feA9kzncOtgfu4HdGfHKMWD9rTN1tGt05aBnfQ7SEU8JxvJrVSKKQVrwB+oSCJSrPPZR5K7I35K3O2NOGsg4TcBLbth90rEHsY//g0E5dBwsO9dCgdwaGAcm8YWsnzOZyLiEPdGg2tz4dm8saV5xoqCznkyZvut3J6aeVvRkWaGJv2S3sD5i99XTJ9unKQFStj/rv4ftS9dEYWN+yDe7LwIZz5P20+9kYWIZOtZ8eiIF7QjDeyeMKrQYwDTO16E1UhPwJMq7pJJMAbX1CXN6DgbaPVvlxmWz3z5Gzkpxwf3QHtuQt1L4ObNrmXg7M4YSrWrOZaJDu5uKbIvwdjtARQvukmrbT3mt3qF15WkJYj/M4D/qv08yWH+eMrxZVbkBfH3kvzDIzvdAsRdSHyJ0oMzTbd5E3GYZvHJlvrDbfuApD14e5WjzlM9ucCE/00NaWz20+4KEtMD7CZm/fw9n/FXh6JPmlMnIG78top3saYJrSQPKW58B7UdA+JdLPey9qyxc7x96Lgr8fOBigjYHyAwf9YB84gL9fODQQMdqIDPWFQ09A2llyV5w8SIrWN7AdKwxViJSolZcOu4Yhx94y0N5h6LTvt0D3Jwzneb9ljY1mhPyAt1vlXGdzu9WwtHcnEsfUpCvNvXe0tiEP9d43XEb7s5gzP19V6Pxwd1y8uP4OP8ds/d8Mxu1/&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

Most of the relationships allowed by the system are `M:N`; what this means, is that given the following:
- Biomaterial/file
- Process

All of the following scenarios are possible
```mermaid
graph TD;
A[Specimen 1]-->B[Dissociation process];
C[Specimen 2]-->B;
B-->D[Pooled cell suspension];

E[Specimen 1]-->F[Dissociation process]
E-->I[Dissociation process 2]
F-->H[Cell suspension 1]
I-->G[Cell suspension 2]
```

```mermaid
graph TD;
A[Cell suspension 1]-->B[Sequencing process]
B-->C[Read 1 sequence file]
B-->D[Read 2 sequence file]
B-->E[Index 1 sequence file]
B-->F[Index 2 sequence file]
```

A general rule of how experiments are modeled in the HCA:
- The input of a process can be one/several biomaterial/files
- The output of a process will be either one biomaterial or one/several files
- A process is unique and cannot be used multiple times.
- (Not shown in figure) A process can have as many protocols attached as needed

Please take into account that there are exceptions; these rules apply to our modelling decisions rather than to limitations
of our system, so if you feel that these rules do not apply to your experiment, please contact us at [the wrangler email](mailto:wrangler-team@data.humancellatlas.org).


## Metadata files in the system

### Ontologised fields

### Extra information

#### _links

## How are 

## 